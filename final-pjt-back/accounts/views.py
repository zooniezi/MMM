from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import *
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import render, get_list_or_404, get_object_or_404

from .serializers import *

# Create your views here.

#############구분선#####################
# 회원탈퇴
@api_view(['DELETE'])
@permission_classes([IsAuthenticated]) # 인증된 사용자만 권한 허용
def user_delete(request):
    request.user.delete()
    data = {
            'content': f'{request.user}님의 탈퇴처리가 완료되었습니다.',
        }
    return Response(data, status=status.HTTP_204_NO_CONTENT)

########################
# 로그인시 유저 정보 조회
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request, username):
    user = get_object_or_404(User, username=username)
    serializer = UserInfoSerializers(user)
    return Response(serializer.data)
