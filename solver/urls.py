from django.urls import path

from . import views

urlpatterns = [
    path("", views.menu, name="index"),
    path("solve/", views.solve, name="solve"),
    path("trainer/", views.trainer, name="trainer"),
]
