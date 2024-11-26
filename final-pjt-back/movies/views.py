from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Feed, Movie, Comment, Emoji

from achievements.models import Achievement

from notifications.models import Notification
from .serializers import FeedSerializer, MovieSerializer, CommentSerializer, EmojiSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db.models import Count, Q
import json
import ast
import random

from django.contrib.auth import get_user_model

# 피드 정보 db저장용
class FeedCreateView(APIView):
    def post(self, request):
        serializer = FeedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # DB에 저장
            # 작성된 Feed 개수 확인
            feed_count = Feed.objects.filter(user=request.user).count()
            
            # 도전과제 - 1: 산뜻한 출발
            if feed_count >= 1:
                # 첫 번째 Feed 작성 시 도전과제 추가
                Achievement.objects.get_or_create(user=request.user, achievement_id=1)


            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 새로운 영화 정보 db저장용
class MovieCreateView(APIView):
    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # DB에 저장
            # 도전과제 - 7: 아무도 등록하지 않았던 영화 등록
            Achievement.objects.get_or_create(user=request.user, achievement_id=7)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

##################################################################################

def get_movie_by_id(request):
    movie = Movie.objects.get(id=request.movie_id)
    data = {
        'id': movie.id,
        'original_title': movie.original_title,
        'overview': movie.overview,
        'poster_path': movie.poster_path,
        'title': movie.title,
        'vote_average': movie.vote_average,
    }

    return JsonResponse(data, safe=False)


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
    user = get_object_or_404(get_user_model(), id=user_id)
    # 사용자 ID에 해당하는 Feed 데이터 가져오기
    feeds = Feed.objects.filter(user_id=user_id)

    # 도전과제 8~26 : 장르별 영화 10개 등록
    mystery_feeds = feeds.filter(genre_ids__regex=r'\b9648\b').count()
    action_feeds = feeds.filter(genre_ids__regex=r'\b28\b').count()
    adventure_feeds = feeds.filter(genre_ids__regex=r'\b12\b').count()
    animation_feeds = feeds.filter(genre_ids__regex=r'\b16\b').count()
    comedy_feeds = feeds.filter(genre_ids__regex=r'\b35\b').count()
    crime_feeds = feeds.filter(genre_ids__regex=r'\b80\b').count()
    documentary_feeds = feeds.filter(genre_ids__regex=r'\b99\b').count()
    drama_feeds = feeds.filter(genre_ids__regex=r'\b18\b').count()
    family_feeds = feeds.filter(genre_ids__regex=r'\b10751\b').count()
    fantasy_feeds = feeds.filter(genre_ids__regex=r'\b14\b').count()
    history_feeds = feeds.filter(genre_ids__regex=r'\b36\b').count()
    horror_feeds = feeds.filter(genre_ids__regex=r'\b27\b').count()
    musical_feeds = feeds.filter(genre_ids__regex=r'\b10402\b').count()
    romance_feeds = feeds.filter(genre_ids__regex=r'\b10749\b').count()
    sf_feeds = feeds.filter(genre_ids__regex=r'\b878\b').count()
    tvmovie_feeds = feeds.filter(genre_ids__regex=r'\b10770\b').count()
    thriller_feeds = feeds.filter(genre_ids__regex=r'\b53\b').count()
    war_feeds = feeds.filter(genre_ids__regex=r'\b10752\b').count()
    western_feeds = feeds.filter(genre_ids__regex=r'\b37\b').count()

    # 조건에 따라 Achievement 생성
    if mystery_feeds >= 10:
        Achievement.objects.get_or_create(user=user, achievement_id=8)

    if horror_feeds >= 10:
        Achievement.objects.get_or_create(user=user, achievement_id=9)

    if action_feeds >= 10:
        Achievement.objects.get_or_create(user=user, achievement_id=10)

    if adventure_feeds >= 10:
        Achievement.objects.get_or_create(user=user, achievement_id=11)

    if animation_feeds >= 10:
        Achievement.objects.get_or_create(user=user, achievement_id=12)

    if comedy_feeds >= 10:
        Achievement.objects.get_or_create(user=user, achievement_id=13)

    if crime_feeds >= 10:
        Achievement.objects.get_or_create(user=user, achievement_id=14)

    if documentary_feeds >= 10:
        Achievement.objects.get_or_create(user=user, achievement_id=15)

    if drama_feeds >= 10:
        Achievement.objects.get_or_create(user=user, achievement_id=16)

    if family_feeds >= 10:
        Achievement.objects.get_or_create(user=user, achievement_id=17)

    if fantasy_feeds >= 10:
        Achievement.objects.get_or_create(user=user, achievement_id=18)

    if history_feeds >= 10:
        Achievement.objects.get_or_create(user=user, achievement_id=19)

    if musical_feeds >= 10:
        Achievement.objects.get_or_create(user=user, achievement_id=20)

    if romance_feeds >= 10:
        Achievement.objects.get_or_create(user=user, achievement_id=21)

    if sf_feeds >= 10:
        Achievement.objects.get_or_create(user=user, achievement_id=22)

    if tvmovie_feeds >= 10:
        Achievement.objects.get_or_create(user=user, achievement_id=23)

    if thriller_feeds >= 10:
        Achievement.objects.get_or_create(user=user, achievement_id=24)

    if war_feeds >= 10:
        Achievement.objects.get_or_create(user=user, achievement_id=25)

    if western_feeds >= 10:
        Achievement.objects.get_or_create(user=user, achievement_id=26)

    # 도전과제 - 27 : 모든 평점 등록
    rating_one_exists = feeds.filter(rating=1).exists()
    rating_two_exists = feeds.filter(rating=2).exists()
    rating_three_exists = feeds.filter(rating=3).exists()
    rating_four_exists = feeds.filter(rating=4).exists()
    rating_five_exists = feeds.filter(rating=5).exists()
    has_all_rating = all([rating_one_exists,rating_two_exists,rating_three_exists,rating_four_exists,rating_five_exists])
    if has_all_rating:
        Achievement.objects.get_or_create(user=user, achievement_id=27)

    # 도전과제 - 3 : 계절별로 영화 보기
    winter_exists = feeds.filter(watch_date__month__in=[12, 1, 2]).exists()
    spring_exists = feeds.filter(watch_date__month__in=[3, 4, 5]).exists()
    summer_exists = feeds.filter(watch_date__month__in=[6, 7, 8]).exists()
    autumn_exists = feeds.filter(watch_date__month__in=[9, 10, 11]).exists()

    # 모든 계절이 존재하는지 확인
    has_all_seasons = all([winter_exists, spring_exists, summer_exists, autumn_exists])
    if has_all_seasons:
        Achievement.objects.get_or_create(user=user, achievement_id=3)

    # 도전과제 - 6,11 : 영화 등록 수 100개, 1000개 돌파
    feed_count = feeds.count()
    if feed_count >= 100:
        Achievement.objects.get_or_create(user=user, achievement_id=6)
    if feed_count >= 1000:
        Achievement.objects.get_or_create(user=user, achievement_id=11)
    # 도전과제 - 4: 혼자서 영화 10개 이상 보기
    feed_count = Feed.objects.filter(user_id=user_id,watch_with_who='혼자').count()
    if feed_count >= 10:
        Achievement.objects.get_or_create(user=user, achievement_id=4)
    # 도전과제 - 5: 연인과 영화 10개 이상 보기
    feed_count = Feed.objects.filter(user_id=user_id,watch_with_who='연인').count()
    if feed_count >= 10:
        Achievement.objects.get_or_create(user=user, achievement_id=5)

    

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

# 프로필 페이지 피드 출력용
def feed_recommend_at_home(request, user_id):
    
    if not Feed.objects.filter(user_id=user_id).exists():
        feeds = Feed.objects.all().order_by('-rating')[:100]
        random_feed = random.choice(feeds)
        random_movie_info = Movie.objects.get(id=random_feed.movie_id)
        data = [
            {
                "movie_id" : random_movie_info.id,
                "movie_title" : random_movie_info.title,
                "movie_overview" : random_movie_info.overview,
                "movie_posterpath" : random_movie_info.poster_path,
                "related_movie_title" : None,
            }
        ]
        return JsonResponse(data,safe=False)

    # 사용자 ID에 해당하는 Feed 데이터 가져오기
    
    feeds = Feed.objects.filter(user_id=user_id)
    
    genre_check = {
        28: 0,
        12: 0,
        16: 0,
        35: 0,
        80: 0,
        99: 0,
        18: 0,
        10751: 0,
        14: 0,
        36: 0,
        27: 0,
        10402: 0,
        9648: 0,
        10749: 0,
        878:0,
        10770:0,
        53:0,
        10752:0,
        37:0,
    }
    movie_id_check = {
        28: [],
        12: [],
        16: [],
        35: [],
        80: [],
        99: [],
        18: [],
        10751: [],
        14: [],
        36: [],
        27: [],
        10402: [],
        9648: [],
        10749: [],
        878:[],
        10770:[],
        53:[],
        10752:[],
        37:[],
    }
    # JSON 형태로 반환할 데이터 구성
    data = []
    for feed in feeds:
        # Movie 데이터 가져오기 (포스터 url)
        for genre in feed.genre_ids:
            genre_check[genre] += 1
            movie_id_check[genre].append(feed.movie_id)

    most_viewed_genres = random.choice([key for key,value in genre_check.items() if max(genre_check.values()) == value])
    def get_random_feed(genre_ids, user_id):
        query = ~Q(user_id=user_id)
        randomfeeds = Feed.objects.filter(query)
        choosefeeds = []
        for feed in randomfeeds:
            feed_genre_ids = json.loads(feed.genre_ids) if isinstance(feed.genre_ids, str) else feed.genre_ids
            if most_viewed_genres in feed_genre_ids:
                choosefeeds.append(feed)

        return random.choice(choosefeeds)
    data = []

    chosen_feed = get_random_feed(most_viewed_genres, user_id)
    related_feed_movie_id = random.choice(movie_id_check[most_viewed_genres])
    chosen_movie_info = Movie.objects.get(id=chosen_feed.movie_id)

    related_movie_title = Movie.objects.get(id=related_feed_movie_id).title

    data = [
        {
            "movie_id" : chosen_movie_info.id,
            "movie_title" : chosen_movie_info.title,
            "movie_overview" : chosen_movie_info.overview,
            "movie_posterpath" : chosen_movie_info.poster_path,
            "related_movie_title" : related_movie_title,
        }
    ]

    return JsonResponse(data, safe=False)







##################################################################################
############################## 추천 알고리즘 #####################################

def get_similar_feeds(watch_time, watch_with_who, genre_ids, user_id=None):
    query = ~Q(user_id=user_id)
    # 기본 필터로 데이터 조회
    feeds = Feed.objects.filter(query)
    
    if isinstance(genre_ids, int):
        genre_ids = [genre_ids]
    # Python에서 genre_ids 조건 처리
    if genre_ids:
        filtered_feeds = []
        for feed in feeds:
            # if genre_ids in feed.genre_ids:
            #     filtered_feeds.append(feed)
            # JSON 문자열을 Python 리스트로 변환
            try:
                feed_genre_ids = json.loads(feed.genre_ids) if isinstance(feed.genre_ids, str) else feed.genre_ids
            except json.JSONDecodeError:
                continue  # JSON 파싱 실패 시 해당 레코드 무시

            # genre_ids의 교집합 확인
            if any(genre in feed_genre_ids for genre in genre_ids):
                filtered_feeds.append(feed)
        return filtered_feeds

# 입력과 같은 조건의 영화들 불러오기
def get_matched_feeds(watch_time, watch_with_who, genre_ids, user_id=None):
    # 기본 필터 조건
    query = Q(watch_time=watch_time) & Q(watch_with_who=watch_with_who)

    # 본인이 작성한 기록은 제외
    if user_id:
        query &= ~Q(user_id=user_id)

    # 기본 필터로 데이터 조회
    feeds = Feed.objects.filter(query)
    
    if isinstance(genre_ids, int):
        genre_ids = [genre_ids]
    # if genre_ids:
    #     filtered_feeds = []
    #     for feed in feeds:
    #         if genre_ids in feed.genre_ids:
    #             filtered_feeds.append(feed)

    # Python에서 genre_ids 조건 처리
    if genre_ids:
        filtered_feeds = []
        for feed in feeds:
            # JSON 문자열을 Python 리스트로 변환
            try:
                feed_genre_ids = json.loads(feed.genre_ids) if isinstance(feed.genre_ids, str) else feed.genre_ids
            except json.JSONDecodeError:
                continue  # JSON 파싱 실패 시 해당 레코드 무시

            # genre_ids의 교집합 확인
            if any(genre in feed_genre_ids for genre in genre_ids):
                filtered_feeds.append(feed)
        return filtered_feeds

    return feeds



def recommend_movies_upgrade(request):
    user_id = request.GET.get('user_id')  # 사용자 ID
    watch_time = request.GET.get('watch_time')  # 예: 'morning'
    watch_with_who = request.GET.get('watch_with_who')  # 예: 'friends'
    genre_ids_temp = request.GET.getlist('genre_id')  # 예: [28, 12]
    genre_ids = int(genre_ids_temp[0])
    selected_rating = request.GET.get('selected_rating')
    # 문자열 자료 숫자로 변환하기
    # for ids in genre_ids_temp:
    #     genre_ids = int(ids)

    similar_feeds = get_similar_feeds(watch_time, watch_with_who, genre_ids, user_id)
    matched_feeds = get_matched_feeds(watch_time, watch_with_who, genre_ids, user_id)
    
    # 확인용 
    # print('similar feeds found : ',len(similar_feeds))
    # print('matched_feeds found : ', len(matched_feeds))
    
    # 중복된 영화는 제외하고 추천
    recommended_movies = {}
    for feed in matched_feeds:
        if feed.movie_id not in recommended_movies:
            recommended_movies[feed.movie_id] = {
                "movie_id": feed.movie_id,
                "genres": feed.genre_ids,
                "rating": feed.rating,
                "comment": feed.comment,
            }
    if len(recommended_movies) <= 10:   
        for feed in similar_feeds:
            if feed.movie_id not in recommended_movies:
                recommended_movies[feed.movie_id] = {
                    "movie_id": feed.movie_id,
                    "genres": feed.genre_ids,
                    "rating": feed.rating,
                    "comment": feed.comment,
                }
    # 높은 평점 순으로 정렬된 추천 리스트 반환
    recommend_movies_candidate = sorted(recommended_movies.values(), key=lambda x: x["rating"], reverse=True)

    # rating별 인덱스 범위를 계산
    from collections import defaultdict

    def get_rating_ranges(data):
        rating_ranges = defaultdict(list)
        for index, item in enumerate(data):
            rating = item['rating']
            rating_ranges[rating].append(index)

        # 각 rating의 첫 번째와 마지막 인덱스 계산
        result = {5:(-1,-1),4:(-1,-1),3:(-1,-1),2:(-1,-1),1:(-1,-1)}
        for rating, indices in rating_ranges.items():
            result[rating] = (min(indices), max(indices))

        return result

    # 실행
    rating_ranges = get_rating_ranges(recommend_movies_candidate)

    can_recommend_index = rating_ranges[int(selected_rating)][1]
    
    if can_recommend_index >= 5:
        sample_recommend_movies = random.sample(recommend_movies_candidate[:can_recommend_index+1],5)
    else:
        sample_recommend_movies = recommend_movies_candidate

    # 추천 목록에 해당하는 영화 데이터 가져오기
    movie_ids = [rec['movie_id'] for rec in sample_recommend_movies]

    if movie_ids:
        movies = Movie.objects.filter(id__in=movie_ids)
    else:
        movies = [] 

    data = []
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
    random.shuffle(data)
    return JsonResponse(data, safe=False)


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
            # 도전과제 - 2: 이모지 10개 이상 받기
            if emoji.count() >= 10:
                Achievement.objects.get_or_create(user=user, achievement_id=2)
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
