from django.urls import path, include
from . import views

app_name = 'accounts'
# signup(POST) : account/signup/
# 유저정보 수정하기(GET/PUT) : account/user
# 비밀번호 번경하기(POST) : account/password/change/
# 비밀번호 찾기(POST) : account/password/reset/



urlpatterns = [
    path('userinfo/<str:username>/', views.get_user_info), # 로그인 했을 때 유저 정보 조회
    path('delete/', views.user_delete, name='user_delete'), # 회원탈퇴
    path('follow/<str:username>/', views.follow, name='follow'),
    path('follow/list/<str:username>/', views.get_follows),
]
