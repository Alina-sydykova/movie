# movies/views.py

import json

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .services import search_movies_api, get_movie_detail_api
from .models import FavoriteMovie


# ========== ГЛАВНАЯ СТРАНИЦА ==========

def home(request):
    """
    Главная страница: баннер + поиск по фильмам (OMDb).
    Для залогиненного пользователя дополнительно передаём favorite_ids
    (список imdb_id, которые уже в избранном) — для сердечек.
    """
    query = request.GET.get("q", "").strip()
    movies = []

    if query:
        try:
            movies = search_movies_api(query)
        except Exception:
            movies = []
            messages.error(request, "Не удалось загрузить фильмы. Попробуйте ещё раз.")

    favorite_ids = []
    if request.user.is_authenticated:
        favorite_ids = list(
            FavoriteMovie.objects.filter(user=request.user)
            .values_list("imdb_id", flat=True)
        )

    context = {
        "query": query,
        "movies": movies,
        "favorite_ids": favorite_ids,
    }
    return render(request, "movies/index.html", context)


# ========== ДЕТАЛИ ФИЛЬМА ==========

def movie_detail(request, imdb_id):
    """
    Страница детали фильма: постер, описание, актёры, рейтинг и т.п.
    """
    if not imdb_id or imdb_id == "undefined":
        return redirect("home")

    movie = get_movie_detail_api(imdb_id)
    if not movie:
        messages.error(request, "Фильм не найден.")
        return redirect("home")

    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = FavoriteMovie.objects.filter(
            user=request.user, imdb_id=imdb_id
        ).exists()

    return render(
        request,
        "movies/detail.html",
        {"movie": movie, "is_favorite": is_favorite},
    )


# ========== ИЗБРАННОЕ (СТРАНИЦА) ==========

@login_required
def favorites(request):
    """
    Страница "Мои избранные": список всех избранных фильмов текущего пользователя.
    """
    favorites_qs = FavoriteMovie.objects.filter(user=request.user).order_by("-id")
    return render(request, "movies/favorites.html", {"favorites": favorites_qs})


# ========== ДОБАВЛЕНИЕ / УДАЛЕНИЕ (КЛАССИЧЕСКИЕ URL) ==========

@login_required
def add_to_favorites(request, imdb_id):
    """
    Добавление фильма в избранное через обычный URL (без AJAX).
    Можно вызывать с кнопки "Добавить в избранное" на detail-странице.
    """
    movie = get_movie_detail_api(imdb_id)
    if not movie:
        messages.error(request, "Не удалось добавить фильм.")
        return redirect("home")

    fav, created = FavoriteMovie.objects.get_or_create(
        user=request.user,
        imdb_id=imdb_id,
        defaults={
            "title": movie.get("Title", ""),
            "poster": movie.get("Poster", ""),
            "year": movie.get("Year", ""),
        },
    )

    if created:
        messages.success(request, "Фильм добавлен в избранное.")
    else:
        messages.info(request, "Этот фильм уже в избранном.")

    return redirect(request.META.get("HTTP_REFERER", "/"))


@login_required
def remove_from_favorites(request, imdb_id):
    """
    Удаление фильма из избранного через обычный URL.
    """
    FavoriteMovie.objects.filter(
        user=request.user,
        imdb_id=imdb_id,
    ).delete()
    messages.info(request, "Фильм удалён из избранного.")
    return redirect(request.META.get("HTTP_REFERER", "/"))


# ========== AJAX TOGGLE ДЛЯ СЕРДЕЧКА ==========

@require_POST
@login_required
def toggle_favorite(request):
    """
    AJAX-обработчик для одной иконки-сердечка:
      - если фильма нет в избранном → добавить
      - если есть → удалить
    Возвращает JSON: {"status": "added"} или {"status": "removed"}.
    """
    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Bad JSON"}, status=400)

    imdb_id = data.get("imdb_id")
    if not imdb_id:
        return JsonResponse({"status": "error", "message": "No imdb_id"}, status=400)

    title = data.get("title", "")
    year = data.get("year", "")
    poster = data.get("poster") or ""

    fav, created = FavoriteMovie.objects.get_or_create(
        user=request.user,
        imdb_id=imdb_id,
        defaults={
            "title": title,
            "year": year,
            "poster": poster,
        },
    )

    if created:
        return JsonResponse({"status": "added"})

    # уже было в избранном → удаляем
    fav.delete()
    return JsonResponse({"status": "removed"})


# ========== ЛИЧНЫЙ КАБИНЕТ ==========

@login_required
def profile(request):
    """
    Простой личный кабинет: можно вывести статистику, имя и т.п.
    """
    fav_count = FavoriteMovie.objects.filter(user=request.user).count()
    return render(request, "movies/profile.html", {"fav_count": fav_count})


# ========== ПРОЧИЕ РАЗДЕЛЫ (СЕРИАЛЫ / НОВОСТИ / КАЛЕНДАРЬ) ==========

@login_required
def series_page(request):
    return render(request, "movies/series.html")


@login_required
def news_page(request):
    return render(request, "movies/news.html")


@login_required
def calendar_page(request):
    return render(request, "movies/calendar.html")


# ========== РЕГИСТРАЦИЯ ==========

def register(request):
    """
    Регистрация нового пользователя.
    После успешной регистрации сразу логиним и отправляем на главную.
    """
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()

    return render(request, "registration/register.html", {"form": form})
