# movie_catalog/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    # Основные страницы (главная, избранное и т.д.)
    path("", include("movies.urls")),

    # Логин/логаут Django
    path("accounts/", include("django.contrib.auth.urls")),

    # Переключение языка (set_language)
    path("i18n/", include("django.conf.urls.i18n")),
    


    # API для фронта
    path("api/", include("movies.api_urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
