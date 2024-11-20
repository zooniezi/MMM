from django.urls import path
from .views import FeedCreateView, MovieCreateView

app_name = 'movies'

urlpatterns = [
    path('feed/create/', FeedCreateView.as_view(), name='feed_create'),
    path('movie/create/', MovieCreateView.as_view(), name='movie_create'),
]
