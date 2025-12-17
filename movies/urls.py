# # movies/urls.py
# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.index, name='home'),
#     path('movie/<str:imdb_id>/', views.movie_detail, name='detail'),

#     # избранное
#     path('favorites/', views.favorites_list, name='favorites'),
#     path('favorites/add/<str:imdb_id>/', views.add_to_favorites, name='add_fav'),
#     path('favorites/remove/<str:imdb_id>/', views.remove_from_favorites, name='remove_fav'),
# ]





# urlpatterns = [
#     path("", views.index, name="home"),
#     path("movie/<str:imdb_id>/", views.movie_detail, name="detail"),

#     path("favorites/add/<str:imdb_id>/", views.add_to_favorites, name="add_fav"),
#     path("favorites/remove/<str:imdb_id>/", views.remove_from_favorites, name="remove_fav"),
#     path("favorites/", views.favorites_list, name="favorites"),

#     path("series/", views.series_page, name="series"),
#     path("news/", views.news_page, name="news"),
#     path("calendar/", views.calendar_page, name="calendar"),
#     path("profile/", views.profile_page, name="profile"),
# ]




# from django.urls import path
# from . import views

# urlpatterns = [
#     path("", views.home, name="home"),
#     path("movie/<str:imdb_id>/", views.movie_detail, name="movie_detail"),
#     path("favorites/add/<str:imdb_id>/", views.add_to_favorites, name="add_to_favorites"),
#     path("favorites/", views.favorites, name="favorites"),
#     path("profile/", views.profile, name="profile"),
# ]



# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.home, name='home'),
#     path('series/', views.series, name='series'),
#     path('news/', views.news, name='news'),
#     path('calendar/', views.calendar, name='calendar'),

#     path('favorites/', views.favorites, name='favorites'),
#     path('favorites/add/<str:imdb_id>/', views.add_to_favorites, name='add_fav'),
#     path('favorites/remove/<str:imdb_id>/', views.remove_from_favorites, name='remove_fav'),
# ]



# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.home, name='home'),

#     path('movie/<str:imdb_id>/', views.movie_detail, name='movie_detail'),

#     path('favorites/', views.favorites, name='favorites'),
#     path('favorites/add/<str:imdb_id>/', views.add_to_favorites, name='add_fav'),
#     path('favorites/remove/<str:imdb_id>/', views.remove_from_favorites, name='remove_fav'),
#     path('favorites/toggle/', views.toggle_favorite, name='toggle_favorite'),

#     path('profile/', views.profile, name='profile'),
#     path('series/', views.series_page, name='series'),
#     path('news/', views.news_page, name='news'),
#     path('calendar/', views.calendar_page, name='calendar'),

#     path('accounts/register/', views.register, name='register'),
# ]


from django.urls import path
from . import views

urlpatterns = [
    # Главная – поиск фильмов
    path("", views.home, name="home"),

    # Страница фильма
    path("movie/<str:imdb_id>/", views.movie_detail, name="movie_detail"),

    # Избранное
    path("favorites/", views.favorites, name="favorites"),
    path("favorites/add/<str:imdb_id>/", views.add_to_favorites, name="add_to_favorites"),
    path("favorites/remove/<str:imdb_id>/", views.remove_from_favorites, name="remove_from_favorites"),

    # Профиль и разделы
    path("profile/", views.profile, name="profile"),
    path("series/", views.series_page, name="series"),
    path("news/", views.news_page, name="news"),
    path("calendar/", views.calendar_page, name="calendar"),
]
