from django.urls import path
from . import views

urlpatterns = [
    path('', views.news_list, name='news_list'),
    path('category/<slug:slug>/', views.news_by_category, name='news_by_category'),
    path('tag/<slug:slug>/', views.news_by_tag, name='news_by_tag'),
    path('<int:pk>/', views.news_detail, name='news_detail'),
]
