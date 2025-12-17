# movies/api_views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .services import search_movies_api, get_movie_detail_api


@api_view(["GET"])
def api_search_movies(request):
    """
    /api/movies/search/?q=...
    Ищем фильмы через OMDb и возвращаем JSON-массив.
    """
    query = request.GET.get("q", "").strip()
    if not query:
        # пустой запрос – просто пустой список
        return Response([], status=status.HTTP_200_OK)

    movies = search_movies_api(query)  # <- твоя функция из services.py
    # movies — это список словарей из OMDb, его можно отдавать как есть
    return Response(movies, status=status.HTTP_200_OK)


@api_view(["GET"])
def api_movie_detail(request, imdb_id: str):
    """
    /api/movies/<imdb_id>/
    Детали фильма по ID (если захочешь использовать на фронте)
    """
    data = get_movie_detail_api(imdb_id)
    if not data:
        return Response({"detail": "Movie not found"}, status=status.HTTP_404_NOT_FOUND)
    return Response(data, status=status.HTTP_200_OK)
