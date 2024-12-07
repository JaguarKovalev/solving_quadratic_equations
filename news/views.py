from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .models import News, Category, Tag
from .forms import NewsForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page

@cache_page(60 * 1)
def news_list(request):
    news_items = News.objects.filter(status='published')
    categories = Category.objects.all()
    tags = Tag.objects.all()
    paginator = Paginator(news_items, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'news/news_list.html', {
        'page_obj': page_obj,
        'categories': categories,
        'tags': tags
    })

@cache_page(60 * 1)
def news_detail(request, pk):
    news = get_object_or_404(News, pk=pk)
    return render(request, 'news/news_detail.html', {'news': news})

@cache_page(60 * 1)
def news_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    news_items = category.news.filter(status='published')
    return render(request, 'news/news_by_category.html', {'category': category, 'news_items': news_items})

@cache_page(60 * 1)
def news_by_tag(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    news_items = tag.news.filter(status='published')
    return render(request, 'news/news_by_tag.html', {'tag': tag, 'news_items': news_items})



@login_required
def create_post(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.status = 'pending'
            post.save()
            form.save_m2m()
            return redirect('news_list')
    else:
        form = NewsForm()
    return render(request, 'news/create_post.html', {'form': form})