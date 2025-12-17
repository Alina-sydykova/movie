# movies/models.py
from django.db import models
from django.contrib.auth.models import User


class FavoriteMovie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='favorite_movies')
    imdb_id = models.CharField(max_length=20)
    title = models.CharField(max_length=255)
    poster = models.URLField(blank=True, null=True)
    year = models.CharField(max_length=10, blank=True)

    class Meta:
        unique_together = ('user', 'imdb_id')

    def __str__(self):
        return f"{self.title} ({self.imdb_id})"


