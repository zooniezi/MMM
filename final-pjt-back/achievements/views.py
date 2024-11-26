from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .models import Achievement
from django.http import JsonResponse
# Create your views here.
def get_user_achievement(request, user_id):
    user = get_object_or_404(get_user_model(), id=user_id)

    achievements = Achievement.objects.filter(user=user)
    data = []

    for achievement in achievements:
        data.append({
            "achievement_id": achievement.achievement_id
        })
    
    return JsonResponse(data, safe=False)