from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import News


def news_list(request):
    news_items = News.objects.all()
    paginator = Paginator(news_items, 4)  # 4 новости на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'news/news_list.html', {'page_obj': page_obj})

def news_detail(request, pk):
    news = get_object_or_404(News, pk=pk)
    return render(request, 'news/news_detail.html', {'news': news})