# movie_catalog/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # Основные страницы (главная, избранное и т.д.)
    path("", include("movies.urls")),

    # Логин/логаут Django
    path("accounts/", include("django.contrib.auth.urls")),

    # API для фронта
    path("api/", include("movies.api_urls")),
]
