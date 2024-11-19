from rest_framework import serializers
from movies.models import *
from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()

# 로그인시 사용자 정보 획득용
class UserInfoSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
        
class UserSerializer(serializers.ModelSerializer): 
    
    class Meta:
        model = User
        fields = ('id', 'username',)



class UserFollowSerializers(serializers.ModelSerializer):
    
    class UserListSerializers(serializers.ModelSerializer):

        class Meta:
            model = User
            fields = ('id', 'username')
            
    followings = UserListSerializers(many=True)
    following_count = serializers.IntegerField(source='followings.count', read_only=True)
    followers = UserListSerializers(many=True)
    follower_count = serializers.IntegerField(source='followers.count', read_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'followers', 'follower_count', 'followings', 'following_count')