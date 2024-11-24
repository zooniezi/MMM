from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    user_send = serializers.StringRelatedField()
    user_receive = serializers.StringRelatedField()

    
    class Meta:
        model = Notification
        fields = [
            'id',
            'user_send',
            'user_receive',
            'feed',
            'message',
            'is_read',
            'created_at',
        ]
