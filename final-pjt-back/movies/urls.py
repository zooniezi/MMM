from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('movie/create/', views.MovieCreateView.as_view(), name='movie_create'),
    path('recommend/', views.recommend_movies_upgrade, name='recommend_movies_with_rating'),

    path('feed/create/', views.FeedCreateView.as_view(), name='feed_create'),
    path('feeds/<int:user_id>/', views.user_feed_list, name='user_feed_list'),
    path('feeds/followed/', views.followed_users_feed_list, name='followed_users_feed_list'),
    path('feeds/recommend/<int:user_id>/', views.feed_recommend_at_home, name='feed_recommend_at_home'),
    path('movies/get/', views.get_movie_by_id, name='get_movie_by_id'),
    # 댓글 조회 및 생성
    path('feeds/<int:feed_id>/comments/', views.comment_list_create, name='comment_list_create'),
    # 댓글 삭제
    path('feeds/<int:feed_id>/comments/<int:comment_id>/', views.comment_delete, name='comment_delete'),
    # 감정 표현 생성 및 삭제
    path('feeds/<int:feed_id>/emoji/', views.toggle_emoji, name='toggle_emoji'),
    # 피드의 모든 감정 표현 조회
    path('feeds/<int:feed_id>/emoji/list/', views.get_feed_emojis, name='get_feed_emojis'),
]
