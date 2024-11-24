from django.db import models
from django.contrib.auth import get_user_model
from movies.models import Feed 

# Create your models here.

User = get_user_model()

class Notification(models.Model):
    user_send = models.ForeignKey(User, on_delete=models.CASCADE, related_name='send_notifications')
    user_receive = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receive_notifications')
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)