# movies/serializers.py
from rest_framework import serializers
from .models import FavoriteMovie


class FavoriteMovieSerializer(serializers.ModelSerializer):
    """
    Модель избранного для API
    """
    class Meta:
        model = FavoriteMovie
        fields = ["id", "imdb_id", "title", "year", "poster_url"]


class MovieShortSerializer(serializers.Serializer):
    """
    Короткая инфа о фильме (поиск)
    """
    imdb_id = serializers.CharField()
    title = serializers.CharField()
    year = serializers.CharField(allow_blank=True, required=False)
    poster_url = serializers.CharField(
        allow_blank=True,
        required=False,
        allow_null=True,
    )


class MovieDetailSerializer(serializers.Serializer):
    """
    Детальная инфа о фильме
    """
    imdb_id = serializers.CharField()
    title = serializers.CharField()
    year = serializers.CharField(allow_blank=True, required=False)
    poster_url = serializers.CharField(
        allow_blank=True,
        required=False,
        allow_null=True,
    )
    plot = serializers.CharField(allow_blank=True, required=False, allow_null=True)
    genre = serializers.CharField(allow_blank=True, required=False, allow_null=True)
    rating = serializers.CharField(allow_blank=True, required=False, allow_null=True)
