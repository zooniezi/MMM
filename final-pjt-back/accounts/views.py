from django.http import JsonResponse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import *
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import render, get_list_or_404, get_object_or_404

from .serializers import *
from .models import User
# Create your views here.

#############구분선#####################
# 회원탈퇴
# transaction 설정을 해야하는가?????
@api_view(['DELETE'])
@permission_classes([IsAuthenticated]) # 인증된 사용자만 권한 허용
def user_delete(request):
    user = request.user

    # 1. 팔로우/팔로워 삭제
    user.followings.clear()  # 내가 팔로우한 사람과의 관계 제거
    user.followers.clear()  # 나를 팔로우한 사람과의 관계 제거

    # 2. 사용자가 작성한 Feed 비공개 처리
    Feed.objects.filter(user=user).update(is_share_to_feed=False)

    username = user.username
    user.delete()

    data = {
            'content': f'{username}님의 탈퇴처리가 완료되었습니다.',
        }
    return Response(data, status=status.HTTP_204_NO_CONTENT)

# 팔로우 기능
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def follow(request, username):
    if request.method=='GET':
        person = get_object_or_404(get_user_model(), username=username)
        user = request.user

        if person != user:
            isFollowed = False
            if person.followers.filter(pk=user.pk).exists():
                isFollowed = True
            return JsonResponse({'isFollowed': isFollowed})
    
    elif request.method == 'POST':
        person = get_object_or_404(get_user_model(), username=username)
        user = request.user
        if person != user:         # 스스로를 팔로우 할 수는 없음
            if person.followers.filter(pk=user.pk).exists():
                # 팔로우 했었는데 다시 팔로우한다 = 언팔로우
                person.followers.remove(user)
                follow = True
            else:
                # 팔로우하지 않았었는데 팔로우한다 = 팔로우
                person.followers.add(user)
                follow = False
            follow_status ={
                'follow':follow,
            }
            return JsonResponse(follow_status)

#################################################################################

def get_users_with_admin(request):
    # 필요한 필드만 선택적으로 가져오기
    users = User.objects.values('id', 'username')
    data = list(users)  # values()는 QuerySet을 반환하므로 list()로 변환

    return JsonResponse(data, safe=False)

def get_users_without_admin(request):
    users = User.objects.filter(is_superuser=False).values('id', 'username', 'is_active')
    data = list(users)
    return JsonResponse(data, safe=False)


# 팔로우팔로워 정보 가져오기
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_follows(request, username):
    user = get_object_or_404(User, username=username)
    serializer = UserFollowSerializers(user, many=False)
    return Response(serializer.data)


########################
# 로그인시 유저 정보 조회
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request, username):
    user = get_object_or_404(User, username=username)
    serializer = UserInfoSerializers(user)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    user = request.user  # 현재 로그인된 사용자
    new_profile = request.data.get('profile')  # 클라이언트로부터 profile 데이터 받기

    if not new_profile:
        return Response({'error': 'Profile content cannot be empty.'}, status=status.HTTP_400_BAD_REQUEST)

    # Profile 업데이트
    user.profile = new_profile
    user.save()

    return Response({'message': 'Profile updated successfully!', 'profile': user.profile}, status=status.HTTP_200_OK)