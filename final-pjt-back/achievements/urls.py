from django.urls import path
from . import views

app_name = 'achievements'

urlpatterns = [
    path('get/<int:user_id>/', views.get_user_achievement, name='get_user_achievement'),
]