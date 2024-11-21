from rest_framework import serializers
from .models import Feed, Movie, Comment, Emoji


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # 댓글 작성자의 username 표시

    class Meta:
        model = Comment
        fields = ['id', 'user', 'emoji', 'content', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

class EmojiSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Emoji
        fields = ['id', 'user', 'feed', 'emoji']
        read_only_fields = ['id', 'user']

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

    def get_movie(self, obj):
        try:
            movie = Movie.objects.get(id=obj.movie_id)
            return {
                'id': movie.id,
                'original_title': movie.original_title,
                'overview': movie.overview,
                'poster_path': movie.poster_path,
                'title': movie.title,
                'vote_average': movie.vote_average,
            }
        except Movie.DoesNotExist:
            return None  # 영화 데이터가 없을 경우 None 반환

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'  # 모든 필드를 직렬화

