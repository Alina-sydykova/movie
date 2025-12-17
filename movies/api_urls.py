# movies/api_urls.py
from django.urls import path
from . import api_views

urlpatterns = [
    path("movies/search/", api_views.api_search_movies, name="api_movies_search"),
    path("movies/<str:imdb_id>/", api_views.api_movie_detail, name="api_movie_detail"),
]
