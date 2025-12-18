# # movies/views.py
# import json

# from django.shortcuts import render, redirect
# from django.contrib import messages
# from django.contrib.auth import login
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserCreationForm
# from django.http import JsonResponse
# from django.views.decorators.http import require_POST

# from .services import search_movies_api, get_movie_detail_api
# from .models import FavoriteMovie


# # ========== ГЛАВНАЯ СТРАНИЦА ==========
# def home(request):
#     query = request.GET.get("q", "").strip()
#     movies = []

#     if query:
#         try:
#             movies = search_movies_api(query)
#         except Exception:
#             movies = []
#             messages.error(request, "Не удалось загрузить фильмы. Попробуйте ещё раз.")

#     favorite_ids = []
#     if request.user.is_authenticated:
#         favorite_ids = list(
#             FavoriteMovie.objects.filter(user=request.user)
#             .values_list("imdb_id", flat=True)
#         )

#     context = {
#         "query": query,
#         "movies": movies,
#         "favorite_ids": favorite_ids,
#     }

#     # ВАЖНО: у тебя шаблон называется index.html (без movies/)
#     return render(request, "index.html", context)


# # ========== ДЕТАЛИ ФИЛЬМА ==========
# def movie_detail(request, imdb_id):
#     if not imdb_id or imdb_id == "undefined":
#         return redirect("home")

#     movie = get_movie_detail_api(imdb_id)
#     if not movie:
#         messages.error(request, "Фильм не найден.")
#         return redirect("home")

#     is_favorite = False
#     if request.user.is_authenticated:
#         is_favorite = FavoriteMovie.objects.filter(
#             user=request.user, imdb_id=imdb_id
#         ).exists()

#     # У тебя файл detail.html лежит рядом, значит так:
#     return render(request, "detail.html", {"movie": movie, "is_favorite": is_favorite})


# # ========== ИЗБРАННОЕ (СТРАНИЦА) ==========
# @login_required
# def favorites(request):
#     favorites_qs = FavoriteMovie.objects.filter(user=request.user).order_by("-id")
#     return render(request, "favorites.html", {"favorites": favorites_qs})


# # ========== ДОБАВЛЕНИЕ / УДАЛЕНИЕ (URL) ==========
# @login_required
# def add_to_favorites(request, imdb_id):
#     movie = get_movie_detail_api(imdb_id)
#     if not movie:
#         messages.error(request, "Не удалось добавить фильм.")
#         return redirect("home")

#     fav, created = FavoriteMovie.objects.get_or_create(
#         user=request.user,
#         imdb_id=imdb_id,
#         defaults={
#             "title": movie.get("Title", ""),
#             "poster": movie.get("Poster", ""),
#             "year": movie.get("Year", ""),
#         },
#     )

#     if created:
#         messages.success(request, "Фильм добавлен в избранное.")
#     else:
#         messages.info(request, "Этот фильм уже в избранном.")

#     return redirect(request.META.get("HTTP_REFERER", "/"))


# @login_required
# def remove_from_favorites(request, imdb_id):
#     FavoriteMovie.objects.filter(user=request.user, imdb_id=imdb_id).delete()
#     messages.info(request, "Фильм удалён из избранного.")
#     return redirect(request.META.get("HTTP_REFERER", "/"))


# # ========== AJAX TOGGLE ==========
# @require_POST
# @login_required
# def toggle_favorite(request):
#     try:
#         data = json.loads(request.body.decode("utf-8"))
#     except json.JSONDecodeError:
#         return JsonResponse({"status": "error", "message": "Bad JSON"}, status=400)

#     imdb_id = data.get("imdb_id")
#     if not imdb_id:
#         return JsonResponse({"status": "error", "message": "No imdb_id"}, status=400)

#     title = data.get("title", "")
#     year = data.get("year", "")
#     poster = data.get("poster") or ""

#     fav, created = FavoriteMovie.objects.get_or_create(
#         user=request.user,
#         imdb_id=imdb_id,
#         defaults={"title": title, "year": year, "poster": poster},
#     )

#     if created:
#         return JsonResponse({"status": "added"})

#     fav.delete()
#     return JsonResponse({"status": "removed"})


# # ========== ЛИЧНЫЙ КАБИНЕТ ==========
# @login_required
# def profile(request):
#     fav_count = FavoriteMovie.objects.filter(user=request.user).count()
#     return render(request, "profile.html", {"fav_count": fav_count})


# # ========== СТРАНИЦЫ (статичные шаблоны) ==========
# @login_required
# def series_page(request):
#     return render(request, "series.html")


# @login_required
# def news_page(request):
#     return render(request, "news.html")


# @login_required
# def calendar_page(request):
#     return render(request, "calendar.html")


# @login_required
# def push_page(request):
#     return render(request, "push.html")


# @login_required
# def follow_page(request):
#     return render(request, "follow.html")


# @login_required
# def mylist_page(request):
#     return render(request, "mylist.html")


# @login_required
# def watch_page(request):
#     return render(request, "watch.html")


# # ========== РЕГИСТРАЦИЯ ==========
# def register(request):
#     if request.method == "POST":
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect("home")
#     else:
#         form = UserCreationForm()

#     return render(request, "registration/register.html", {"form": form})



# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render

# @login_required
# def follow_page(request):
#     return render(request, "movies/follow.html")

# @login_required
# def mylist_page(request):
#     return render(request, "movies/mylist.html")

# @login_required
# def watch_page(request):
#     return render(request, "movies/watch.html")



# movies/views.py
import json
import re
from datetime import timedelta

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Avg, Count
from django.utils import timezone

from .services import search_movies_api, get_movie_detail_api
from .models import FavoriteMovie, MovieRating, Profile, MovieListEntry
from .forms import RegistrationForm, ProfileForm


# ========== ГЛАВНАЯ СТРАНИЦА ==========

def home(request):
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

    context = {"query": query, "movies": movies, "favorite_ids": favorite_ids}
    # ВАЖНО: шаблон теперь просто index.html
    return render(request, "index.html", context)


# ========== ДЕТАЛИ ФИЛЬМА ==========

def movie_detail(request, imdb_id):
    if not imdb_id or imdb_id == "undefined":
        return redirect("home")

    movie = get_movie_detail_api(imdb_id)
    if not movie:
        messages.error(request, "Фильм не найден.")
        return redirect("home")

    is_favorite = False
    is_watch_later = False
    is_family = False
    if request.user.is_authenticated:
        is_favorite = FavoriteMovie.objects.filter(user=request.user, imdb_id=imdb_id).exists()
        is_watch_later = MovieListEntry.objects.filter(
            user=request.user, imdb_id=imdb_id, list_type="watch_later"
        ).exists()
        is_family = MovieListEntry.objects.filter(
            user=request.user, imdb_id=imdb_id, list_type="family"
        ).exists()

    rating_data = MovieRating.objects.filter(imdb_id=imdb_id).aggregate(
        avg=Avg("rating"), count=Count("id")
    )
    user_rating = None
    if request.user.is_authenticated:
        user_rating = (
            MovieRating.objects.filter(user=request.user, imdb_id=imdb_id)
            .values_list("rating", flat=True)
            .first()
        )

    context = {
        "movie": movie,
        "is_favorite": is_favorite,
        "is_watch_later": is_watch_later,
        "is_family": is_family,
        "avg_rating": rating_data.get("avg"),
        "rating_count": rating_data.get("count") or 0,
        "user_rating": user_rating,
        "rating_range": range(1, 11),
    }
    return render(request, "detail.html", context)


# ========== ИЗБРАННОЕ ==========

@login_required
def favorites(request):
    favorites_qs = FavoriteMovie.objects.filter(user=request.user).order_by("-id")
    return render(request, "favorites.html", {"favorites": favorites_qs})


@login_required
def add_to_favorites(request, imdb_id):
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
    FavoriteMovie.objects.filter(user=request.user, imdb_id=imdb_id).delete()
    messages.info(request, "Фильм удалён из избранного.")
    return redirect(request.META.get("HTTP_REFERER", "/"))


@require_POST
def toggle_favorite(request):
    if not request.user.is_authenticated:
        return JsonResponse({"status": "error", "message": "Authentication required"}, status=403)

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
        defaults={"title": title, "year": year, "poster": poster},
    )

    if created:
        return JsonResponse({"status": "added"})

    fav.delete()
    return JsonResponse({"status": "removed"})


# ========== ЛИЧНЫЙ КАБИНЕТ / СТРАНИЦЫ ==========

@login_required
def profile(request):
    fav_count = FavoriteMovie.objects.filter(user=request.user).count()
    profile_obj, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        request.user.first_name = request.POST.get("first_name", "").strip()
        request.user.last_name = request.POST.get("last_name", "").strip()
        email = request.POST.get("email", "").strip()
        if email:
            request.user.email = email
        request.user.save()

        form = ProfileForm(request.POST, request.FILES, instance=profile_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль обновлен.")
        else:
            messages.error(request, "Проверьте данные профиля.")
    else:
        form = ProfileForm(instance=profile_obj)

    context = {
        "fav_count": fav_count,
        "profile_form": form,
        "profile_obj": profile_obj,
    }
    return render(request, "profile.html", context)


@login_required
def series_page(request):
    return render(request, "series.html")


@login_required
def news_page(request):
    return render(request, "news.html")


@login_required
def calendar_page(request):
    return render(request, "calendar.html")


@login_required
def push_page(request):
    return render(request, "push.html")


@login_required
def follow_page(request):
    return render(request, "follow.html")


@login_required
def mylist_page(request):
    return render(request, "mylist.html")


@login_required
def watch_page(request):
    return render(request, "watch.html")


@login_required
def describe_page(request):
    return render(request, "describe.html")


def search_page(request):
    query = request.GET.get("q", "").strip()
    movies = []

    if query:
        try:
            movies = search_movies_api(query)
        except Exception:
            movies = []
            messages.error(request, "Не удалось загрузить фильмы. Попробуйте ещё раз.")

    genre = request.GET.get("genre", "").strip()
    year_filter = request.GET.get("year", "").strip()
    country = request.GET.get("country", "").strip()
    rating_min = request.GET.get("rating_min", "").strip()
    sort = request.GET.get("sort", "").strip() or "relevance"

    genre_options = [
        {"value": "", "label": "Все"},
        {"value": "Action", "label": "Боевик"},
        {"value": "Comedy", "label": "Комедия"},
        {"value": "Drama", "label": "Драма"},
        {"value": "Sci-Fi", "label": "Фантастика"},
        {"value": "Horror", "label": "Ужасы"},
        {"value": "Thriller", "label": "Триллер"},
        {"value": "Romance", "label": "Мелодрама"},
        {"value": "Adventure", "label": "Приключения"},
    ]
    country_options = [
        {"value": "", "label": "Все"},
        {"value": "USA", "label": "США"},
        {"value": "Russia", "label": "Россия"},
        {"value": "Kyrgyzstan", "label": "Кыргызстан"},
        {"value": "Italy", "label": "Италия"},
        {"value": "South Korea", "label": "Южная Корея"},
        {"value": "United Kingdom", "label": "Великобритания"},
    ]
    year_options = ["", "2025", "2024", "2023", "2022", "2021", "2020", "2019", "2018", "2017", "2016", "2015"]
    rating_options = ["", "9", "8", "7", "6", "5"]
    sort_options = [
        {"value": "relevance", "label": "Рекомендованные"},
        {"value": "year_desc", "label": "Год: новые"},
        {"value": "year_asc", "label": "Год: старые"},
        {"value": "rating_desc", "label": "Рейтинг: высокий"},
        {"value": "rating_asc", "label": "Рейтинг: низкий"},
        {"value": "title_asc", "label": "По названию"},
    ]

    def parse_year(value):
        if not value:
            return None
        match = re.search(r"\d{4}", str(value))
        return int(match.group(0)) if match else None

    def parse_float(value):
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    def matches_filter(raw_value, filter_value):
        if not filter_value:
            return True
        if not raw_value:
            return False
        return filter_value.lower() in raw_value.lower()

    results = []
    favorite_ids = []
    watch_later_ids = []
    family_ids = []
    user_ratings = {}
    avg_ratings = {}
    rating_counts = {}

    if movies:
        imdb_ids = [movie.get("imdbID") for movie in movies if movie.get("imdbID")]
        if imdb_ids:
            rating_rows = (
                MovieRating.objects.filter(imdb_id__in=imdb_ids)
                .values("imdb_id")
                .annotate(avg=Avg("rating"), count=Count("id"))
            )
            avg_ratings = {row["imdb_id"]: row["avg"] for row in rating_rows}
            rating_counts = {row["imdb_id"]: row["count"] for row in rating_rows}

            if request.user.is_authenticated:
                user_ratings = {
                    row.imdb_id: row.rating
                    for row in MovieRating.objects.filter(user=request.user, imdb_id__in=imdb_ids)
                }
                favorite_ids = list(
                    FavoriteMovie.objects.filter(user=request.user, imdb_id__in=imdb_ids)
                    .values_list("imdb_id", flat=True)
                )
                watch_later_ids = list(
                    MovieListEntry.objects.filter(
                        user=request.user, imdb_id__in=imdb_ids, list_type="watch_later"
                    ).values_list("imdb_id", flat=True)
                )
                family_ids = list(
                    MovieListEntry.objects.filter(
                        user=request.user, imdb_id__in=imdb_ids, list_type="family"
                    ).values_list("imdb_id", flat=True)
                )

        needs_details = True
        details_map = {}
        if needs_details:
            for movie in movies:
                imdb_id = movie.get("imdbID")
                if not imdb_id:
                    continue
                try:
                    detail = get_movie_detail_api(imdb_id)
                except Exception:
                    detail = None
                if detail:
                    details_map[imdb_id] = detail

        for movie in movies:
            imdb_id = movie.get("imdbID")
            if not imdb_id:
                continue
            detail = details_map.get(imdb_id, {})
            year_value = parse_year(movie.get("Year") or detail.get("Year"))
            imdb_rating = parse_float(detail.get("imdbRating"))
            avg_rating = avg_ratings.get(imdb_id)
            rating_value = avg_rating if avg_rating is not None else (imdb_rating or 0)

            if year_filter and year_value != parse_year(year_filter):
                continue
            if genre and not matches_filter(detail.get("Genre"), genre):
                continue
            if country and not matches_filter(detail.get("Country"), country):
                continue
            if rating_min:
                min_value = parse_float(rating_min) or 0
                if rating_value < min_value:
                    continue

            results.append(
                {
                    "Title": movie.get("Title"),
                    "Year": movie.get("Year"),
                    "imdbID": imdb_id,
                    "Poster": movie.get("Poster"),
                    "Genre": detail.get("Genre"),
                    "Country": detail.get("Country"),
                    "imdbRating": imdb_rating,
                    "avg_rating": avg_rating,
                    "rating_count": rating_counts.get(imdb_id, 0),
                    "user_rating": user_ratings.get(imdb_id),
                    "is_favorite": imdb_id in favorite_ids,
                    "is_watch_later": imdb_id in watch_later_ids,
                    "is_family": imdb_id in family_ids,
                }
            )

        if sort == "year_desc":
            results.sort(key=lambda m: parse_year(m.get("Year")) or 0, reverse=True)
        elif sort == "year_asc":
            results.sort(key=lambda m: parse_year(m.get("Year")) or 0)
        elif sort == "rating_desc":
            results.sort(key=lambda m: m.get("avg_rating") or m.get("imdbRating") or 0, reverse=True)
        elif sort == "rating_asc":
            results.sort(key=lambda m: m.get("avg_rating") or m.get("imdbRating") or 0)
        elif sort == "title_asc":
            results.sort(key=lambda m: (m.get("Title") or "").lower())

    context = {
        "query": query,
        "movies": results,
        "genre": genre,
        "year": year_filter,
        "country": country,
        "rating_min": rating_min,
        "sort": sort,
        "genre_options": genre_options,
        "country_options": country_options,
        "year_options": year_options,
        "rating_options": rating_options,
        "sort_options": sort_options,
    }
    return render(request, "search.html", context)


# ========== РЕГИСТРАЦИЯ ==========

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = RegistrationForm()

    return render(request, "registration/register.html", {"form": form})


@login_required
def subscription_page(request):
    profile = request.user.profile
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "activate":
            plan = request.POST.get("plan", "month")
            profile.subscription_active = True
            profile.subscription_plan = plan
            if plan == "year":
                profile.subscription_until = timezone.now().date() + timedelta(days=365)
            else:
                profile.subscription_until = timezone.now().date() + timedelta(days=30)
            profile.save()
            messages.success(request, "Подписка активирована.")
        elif action == "cancel":
            profile.subscription_active = False
            profile.subscription_plan = ""
            profile.subscription_until = None
            profile.save()
            messages.info(request, "Подписка отменена.")

    return render(request, "subscription.html", {"profile": profile})


@require_POST
def toggle_watch_later(request):
    if not request.user.is_authenticated:
        return JsonResponse({"status": "error", "message": "Authentication required"}, status=403)

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

    entry, created = MovieListEntry.objects.get_or_create(
        user=request.user,
        imdb_id=imdb_id,
        list_type="watch_later",
        defaults={"title": title, "year": year, "poster": poster},
    )

    if created:
        return JsonResponse({"status": "added"})

    entry.delete()
    return JsonResponse({"status": "removed"})


@require_POST
def toggle_family(request):
    if not request.user.is_authenticated:
        return JsonResponse({"status": "error", "message": "Authentication required"}, status=403)

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

    entry, created = MovieListEntry.objects.get_or_create(
        user=request.user,
        imdb_id=imdb_id,
        list_type="family",
        defaults={"title": title, "year": year, "poster": poster},
    )

    if created:
        return JsonResponse({"status": "added"})

    entry.delete()
    return JsonResponse({"status": "removed"})


@login_required
def watch_later_page(request):
    entries = MovieListEntry.objects.filter(
        user=request.user, list_type="watch_later"
    ).order_by("-created_at")
    return render(request, "watch_later.html", {"entries": entries})


@login_required
def family_page(request):
    entries = MovieListEntry.objects.filter(
        user=request.user, list_type="family"
    ).order_by("-created_at")
    return render(request, "family.html", {"entries": entries})


@require_POST
def rate_movie(request):
    if not request.user.is_authenticated:
        return JsonResponse({"status": "error", "message": "Authentication required"}, status=403)

    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Bad JSON"}, status=400)

    imdb_id = data.get("imdb_id")
    rating = data.get("rating")
    if not imdb_id or rating is None:
        return JsonResponse({"status": "error", "message": "Missing data"}, status=400)

    try:
        rating = int(rating)
    except (TypeError, ValueError):
        return JsonResponse({"status": "error", "message": "Bad rating"}, status=400)

    if rating < 1 or rating > 10:
        return JsonResponse({"status": "error", "message": "Out of range"}, status=400)

    title = data.get("title", "")
    year = data.get("year", "")
    poster = data.get("poster") or ""

    MovieRating.objects.update_or_create(
        user=request.user,
        imdb_id=imdb_id,
        defaults={
            "rating": rating,
            "title": title,
            "year": year,
            "poster": poster,
        },
    )

    agg = MovieRating.objects.filter(imdb_id=imdb_id).aggregate(avg=Avg("rating"), count=Count("id"))
    return JsonResponse({"status": "ok", "avg_rating": agg["avg"], "count": agg["count"]})
