from django.urls import path
from .views import FeedCreateView

app_name = 'movies'

urlpatterns = [
    path('feed/create/', FeedCreateView.as_view(), name='feed_create'),
]
