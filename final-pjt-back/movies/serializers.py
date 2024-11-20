from rest_framework import serializers
from .models import Feed, Movie

class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = '__all__'  # 모든 필드 포함


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'  # 모든 필드를 직렬화