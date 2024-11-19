from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Experience(models.Model):
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


