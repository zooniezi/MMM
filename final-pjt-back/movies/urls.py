from django.urls import path
from .views import *

app_name = 'movies'

urlpatterns = [
    path('feed/create/', FeedCreateView.as_view(), name='feed_create'),
    path('movie/create/', MovieCreateView.as_view(), name='movie_create'),
    path('recommend/', recommend_movies_with_rating, name='recommend_movies_with_rating'),
    path('feeds/<int:user_id>/', user_feed_list, name='user_feed_list'),
]
