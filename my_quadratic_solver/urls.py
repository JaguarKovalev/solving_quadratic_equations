from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("solver/", include("solver.urls")),
    path('news/', include('news.urls')),
]
