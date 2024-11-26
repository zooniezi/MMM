from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    profile = models.TextField(blank=True)
    # profile_image = models.ImageField(upload_to='profile_images/', blank=True)
    def __str__(self):
        return self.username
