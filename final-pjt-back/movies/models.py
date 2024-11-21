from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Feed(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    movie_id = models.IntegerField()
    genre_ids = models.JSONField(blank = True, null= True)
    watch_date = models.DateField(auto_now=False, auto_now_add=False)
    watch_time = models.CharField(max_length=50)
    watch_place = models.CharField(max_length=50)
    watch_with_who = models.CharField(max_length=50)
    watch_reason = models.JSONField(blank=True, null=True)
    rating = models.IntegerField()
    comment = models.TextField()
    is_share_to_feed = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

class Movie(models.Model):
    id = models.IntegerField(primary_key=True)  # 영화 ID
    original_title = models.CharField(max_length=255)  # 원제
    overview = models.TextField()  # 줄거리
    poster_path = models.CharField(max_length=255, blank=True, null=True)  # 포스터 경로
    title = models.CharField(max_length=255)  # 영화 제목
    vote_average = models.FloatField()  # 평점

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments')
    feed = models.ForeignKey('Feed', on_delete=models.CASCADE, related_name='comments')
    # 댓글 감정표현
    emoji = models.IntegerField()
    # 쓸지는 모르나 일반적인 댓글처럼 텍스트 데이터도 받아올 수 있도록
    content = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


