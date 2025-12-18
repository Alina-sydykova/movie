# movies/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


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


class Profile(models.Model):
    GENDER_CHOICES = [
        ("M", "М"),
        ("F", "Ж"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.FileField(upload_to="avatars/", blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    phone = models.CharField(max_length=32, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    subscription_active = models.BooleanField(default=False)
    subscription_plan = models.CharField(max_length=50, blank=True)
    subscription_until = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Profile: {self.user.username}"


class MovieRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="movie_ratings")
    imdb_id = models.CharField(max_length=20)
    title = models.CharField(max_length=255, blank=True)
    poster = models.URLField(blank=True, null=True)
    year = models.CharField(max_length=10, blank=True)
    rating = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "imdb_id")

    def __str__(self):
        return f"{self.user.username}: {self.imdb_id} -> {self.rating}"


class MovieListEntry(models.Model):
    LIST_TYPES = [
        ("watch_later", "Посмотрю позже"),
        ("family", "Буду смотреть с семьей"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="movie_lists")
    imdb_id = models.CharField(max_length=20)
    title = models.CharField(max_length=255)
    poster = models.URLField(blank=True, null=True)
    year = models.CharField(max_length=10, blank=True)
    list_type = models.CharField(max_length=20, choices=LIST_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "imdb_id", "list_type")

    def __str__(self):
        return f"{self.user.username}: {self.list_type} -> {self.imdb_id}"


@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        if hasattr(instance, "profile"):
            instance.profile.save()
