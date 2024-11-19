from django.urls import path, include
from . import views

app_name = 'accounts'
# signup : account/signup/
# 

urlpatterns = [
    path('delete/', views.user_delete, name='user_delete'), # 회원탈퇴
]
