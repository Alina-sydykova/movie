# movies/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("movie/<str:imdb_id>/", views.movie_detail, name="movie_detail"),
    path("favorites/", views.favorites, name="favorites"),
    path("favorites/add/<str:imdb_id>/", views.add_to_favorites, name="add_to_favorites"),
    path("favorites/remove/<str:imdb_id>/", views.remove_from_favorites, name="remove_from_favorites"),
    path("favorites/toggle/", views.toggle_favorite, name="toggle_favorite"),
    path("lists/watch-later/toggle/", views.toggle_watch_later, name="toggle_watch_later"),
    path("lists/family/toggle/", views.toggle_family, name="toggle_family"),
    path("ratings/rate/", views.rate_movie, name="rate_movie"),
    path("profile/", views.profile, name="profile"),
    path("subscription/", views.subscription_page, name="subscription"),
    path("series/", views.series_page, name="series"),
    path("news/", views.news_page, name="news"),
    path("calendar/", views.calendar_page, name="calendar"),
    path("push/", views.push_page, name="push"),
    path("follow/", views.follow_page, name="follow"),
    path("mylist/", views.mylist_page, name="mylist"),
    path("mylist/watch-later/", views.watch_later_page, name="watch_later"),
    path("mylist/family/", views.family_page, name="family_list"),
    path("watch/", views.watch_page, name="watch"),
    path("describe/", views.describe_page, name="describe"),
    path("search/", views.search_page, name="search"),
    path("register/", views.register, name="register"),
]
