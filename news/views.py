from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import News, Category, Tag


def news_list(request):
    news_items = News.objects.all()
    categories = Category.objects.all()
    tags = Tag.objects.all()
    paginator = Paginator(news_items, 4)  # 4 новости на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'news/news_list.html', {
        'page_obj': page_obj,
        'categories': categories,
        'tags': tags
    })
def news_detail(request, pk):
    news = get_object_or_404(News, pk=pk)
    return render(request, 'news/news_detail.html', {'news': news})

def news_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    news_items = category.news.all()
    return render(request, 'news/news_by_category.html', {'category': category, 'news_items': news_items})

def news_by_tag(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    news_items = tag.news.all()
    return render(request, 'news/news_by_tag.html', {'tag': tag, 'news_items': news_items})