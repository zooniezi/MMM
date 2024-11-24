from django.urls import path
from . import views

# 기본 주소 = 'notifiactions/'

urlpatterns = [
    path('', views.notification_list, name='notification_list'),
    path('<int:notification_id>/read/', views.mark_as_read, name='mark_as_read'),
]