from django.db.models import Count, F, Avg
from django.db.models.functions import Length
from django.utils.timezone import now, timedelta
from news.models import News, Category, Tag
from solver.models import QuadraticSolution
from django.shortcuts import render

def stats_page(request):
    # Статистика по новостям
    published_posts_count = News.objects.filter(status='published').count()
    longest_post = News.objects.annotate(content_length=Length('content')).order_by('-content_length').first()
    recent_posts_count = News.objects.filter(status='published', created_at__gte=now() - timedelta(days=7)).count()
    posts_with_long_titles = News.objects.annotate(title_length=Length('title'), category_name_length=Length('category__name')).filter(title_length__gt=F('category_name_length')).count()

    # Статистика по уравнениям
    correct_solutions_count = QuadraticSolution.objects.filter(is_correct=True).count()
    most_common_a = QuadraticSolution.objects.values('a').annotate(count=Count('a')).order_by('-count').first()
    recent_solutions = QuadraticSolution.objects.filter(created_at__gte=now() - timedelta(days=7)).count()
    total_solutions = QuadraticSolution.objects.count()
    unique_equations_count = QuadraticSolution.objects.values('a', 'b', 'c').distinct().count()
    correct_solutions = QuadraticSolution.objects.filter(is_correct=True).count()
    accuracy = (correct_solutions / total_solutions * 100) if total_solutions else 0

    context = {
        'published_posts_count': published_posts_count,
        'longest_post': longest_post,
        'recent_posts_count': recent_posts_count,
        'posts_with_long_titles': posts_with_long_titles,
        'correct_solutions_count': correct_solutions_count,
        'most_common_a': most_common_a,
        'recent_solutions': recent_solutions,
        'unique_equations_count': unique_equations_count,
        'accuracy': accuracy,
    }
    return render(request, 'stats/stats_page.html', context)
