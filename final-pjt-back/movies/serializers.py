from rest_framework import serializers
from .models import Feed, Movie, Comment


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # 댓글 작성자의 username 표시

    class Meta:
        model = Comment
        fields = ['id', 'user', 'emoji', 'content', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
        extra_kwargs = {
            'content': {'required': False, 'allow_null': True}  # content 필드 선택적 설정
        }

class FeedSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    movie = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)  # 댓글 목록 추가

    class Meta:
        model = Feed
        fields = [
            'id',
            'user',
            'movie_id',
            'movie',
            'genre_ids',
            'watch_date',
            'watch_time',
            'watch_place',
            'watch_with_who',
            'watch_reason',
            'rating',
            'comment',
            'is_share_to_feed',
            'created_at',
            'comments',  # 댓글 목록 포함
        ]


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'  # 모든 필드를 직렬화

