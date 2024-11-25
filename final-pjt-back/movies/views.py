from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Feed, Movie, Comment, Emoji
from notifications.models import Notification
from .serializers import FeedSerializer, MovieSerializer, CommentSerializer, EmojiSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db.models import Count


# 피드 정보 db저장용
class FeedCreateView(APIView):
    def post(self, request):
        serializer = FeedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # DB에 저장
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 새로운 영화 정보 db저장용
class MovieCreateView(APIView):
    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # DB에 저장
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

##################################################################################

@api_view(['GET'])
@permission_classes([IsAuthenticated])
# 피드 페이지 피드 출력용 (팔로우한 사람들의 피드 최신순 출력)
def followed_users_feed_list(request):
    user = request.user
    followed_users = user.followings.all()

    feeds = Feed.objects.filter(user__in=followed_users, is_share_to_feed=True).order_by('-created_at')[:50]
    feed_data = []
    for feed in feeds:
        try:
            movie = Movie.objects.get(id=feed.movie_id)
            movie_data = {
                'id': movie.id,
                'original_title': movie.original_title,
                'overview': movie.overview,
                'poster_path': movie.poster_path,
                'title': movie.title,
                'vote_average': movie.vote_average,
            }
        except Movie.DoesNotExist:
            movie_data = None  # 또는 기본값 설정

        serialized_feed = FeedSerializer(feed).data
        serialized_feed['movie'] = movie_data
        feed_data.append(serialized_feed)

    return JsonResponse(feed_data, safe=False)

# 프로필 페이지 피드 출력용
def user_feed_list(request, user_id):
    # 사용자 ID에 해당하는 Feed 데이터 가져오기
    feeds = Feed.objects.filter(user_id=user_id)

    # JSON 형태로 반환할 데이터 구성
    data = []
    for feed in feeds:
        # Movie 데이터 가져오기 (포스터 url)
        try:
            movie = Movie.objects.get(id=feed.movie_id)
            poster_path = movie.poster_path  # Movie의 poster_path 가져오기
            title = movie.title
            original_title = movie.original_title
        except Movie.DoesNotExist:
            poster_path = None  # Movie 데이터가 없을 경우 None 처리

        # Feed 데이터에 poster_path 추가
        data.append({
            "id": feed.id,
            "movie_title": title,
            "movie_id": feed.movie_id,
            "genre_ids": feed.genre_ids,
            "watch_date": feed.watch_date,
            "watch_time": feed.watch_time,
            "watch_place": feed.watch_place,
            "watch_with_who": feed.watch_with_who,
            "watch_reason": feed.watch_reason,
            "rating": feed.rating,
            "comment": feed.comment,
            "is_share_to_feed": feed.is_share_to_feed,
            "poster_path": poster_path,  # 추가된 필드
        })

    return JsonResponse(data, safe=False)

##################################################################################

# 사용자의 입력 기반 영화 추천
def recommend_movies_with_rating(request):
    user_id = request.GET.get('user_id')  # 사용자 ID
    watch_time = request.GET.get('watch_time')  # 예: 'morning'
    watch_with_who = request.GET.get('watch_with_who')  # 예: 'friends'
    genre_ids_temp = request.GET.getlist('genre_id')  # 예: [28, 12]
    genre_ids = []

    # 문자열 자료 숫자로 변환하기
    for ids in genre_ids_temp:
        genre_ids.append(int(ids))

    data = []
    # Feed 데이터 가져오기-일단 전부 가져오기
    feeds = Feed.objects.all()

    # 사용자가 봤던 영화는 다시 추천할 필요가 없기에 시청했던 영화 목록 가져오기
    already_watched_movies = Feed.objects.filter(user_id=user_id).values_list('movie_id', flat=True) # flat은 리스트로 받기위해서

    # 추천결과 저장용 리스트
    recommendations = []

    for feed in feeds:
        # 사용자가 이미 시청한 영화는 추천 대상에서 제외
        if feed.movie_id in already_watched_movies:
            continue

        # 추천 여부를 결정할 척도인 score 선언
        score = 0
        # 기본 조건에 따른 점수 부여
        #
        if feed.watch_time == watch_time:
            score += 2
        if feed.watch_with_who == watch_with_who:
            score += 5
        if set(feed.genre_ids).intersection(set(genre_ids)):
            score += 5

        # rating 기반 가중치 추가
        score += feed.rating*2  

        # 일정수준 이상이면 추천 목록 후보에 추가
        if score > 10:
            recommendations.append((feed.movie_id, score))

    # 추천 목록 후보가 10개 이하인 경우 vote_average를 이용해 추천 목록 10개까지 채우기
    additional_movies = []
    if len(recommendations) < 5:
        additional_movies = Movie.objects.exclude(
        id__in=[rec[0] for rec in recommendations]
    ).exclude(
        id__in=already_watched_movies
    ).order_by('-vote_average')[:5 - len(recommendations)]


    # 점수 순으로 정렬하고 상위 10개 추출
    recommendations = sorted(recommendations, key=lambda x: x[1], reverse=True)[:10]

    # 추천 목록에 해당하는 영화 데이터 가져오기
    movie_ids = [rec[0] for rec in recommendations]

    if movie_ids:
        movies = Movie.objects.filter(id__in=movie_ids)
    else:
        movies = [] 

    # 결과 반환
    data = [
        {
            "id": movie.id,
            "original_title": movie.original_title,
            "overview": movie.overview,
            "poster_path": movie.poster_path,
            "title": movie.title,
            "vote_average": movie.vote_average,
        }
        for movie in movies
    ]
    for movie in additional_movies:
        data.append({
            "id": movie.id,
            "original_title": movie.original_title,
            "overview": movie.overview,
            "poster_path": movie.poster_path,
            "title": movie.title,
            "vote_average": movie.vote_average,
        })

    return JsonResponse(data, safe=False)

################################################################


# 댓글 조회 및 생성
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def comment_list_create(request, feed_id):
    feed = get_object_or_404(Feed, id=feed_id)
    serializer = CommentSerializer(data=request.data, context={'feed': feed, 'request': request})
    # 특정 Feed에 대한 댓글 조회
    if request.method == 'GET':
        comments = Comment.objects.filter(feed_id=feed_id).order_by('-created_at')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    # 댓글 생성
    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(feed_id=feed_id, user=request.user)
            if feed.user != request.user:
                Notification.objects.create(
                    user_send = request.user,
                    user_receive = feed.user,
                    feed = feed,
                    message = f"{request.user.username} 님이 당신의 피드에 댓글을 남겼습니다."
                )
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

# 댓글 삭제용
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def comment_delete(request, feed_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, feed_id=feed_id, user=request.user)
    comment.delete()
    return Response({"message": "Comment deleted successfully."}, status=HTTP_204_NO_CONTENT)

# 감정 표현 추가/삭제용
@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def toggle_emoji(request, feed_id):
    user = request.user
    emoji_value = request.data.get('emoji')  # 전달된 이모지 값

    # Feed 객체 가져오기
    feed = Feed.objects.filter(id=feed_id).first()
    # 못찾아올때 에러메세지
    if not feed:
        return Response({'error': 'Feed not found.'}, status=status.HTTP_404_NOT_FOUND)

    # 감정 표현 조회 (GET)
    if request.method == 'GET':
        try:
            emoji = Emoji.objects.get(user=user, feed=feed)
            return Response({'emoji': emoji.emoji}, status=status.HTTP_200_OK)
        except Emoji.DoesNotExist:
            return Response({'emoji': None}, status=status.HTTP_200_OK)
        
    # 감정 표현 추가 시
    if request.method == 'POST':
        emoji, created = Emoji.objects.get_or_create(user=user, feed=feed, defaults={'emoji': emoji_value})
        if not created:
            return Response({'message': 'Emoji already exists for this feed.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = EmojiSerializer(emoji)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # 감정 표현 삭제 시
    elif request.method == 'DELETE':
        try:
            emoji = Emoji.objects.get(user=user, feed=feed)
            emoji.delete()
            return Response({'message': 'Emoji removed successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except Emoji.DoesNotExist:
            return Response({'error': 'Emoji not found for this user and feed.'}, status=status.HTTP_404_NOT_FOUND)

# 피드별 이모지 조회용
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_feed_emojis(request, feed_id):
    feed = Feed.objects.filter(id=feed_id).first()
    # 없으면 에러
    if not feed:
        return Response({'error': 'Feed not found.'}, status=status.HTTP_404_NOT_FOUND)

    emojis = Emoji.objects.filter(feed=feed)
    serializer = EmojiSerializer(emojis, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
