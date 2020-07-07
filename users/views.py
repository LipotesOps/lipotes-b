import uuid

from django.shortcuts import render
from django.contrib.auth import get_user_model

from rest_framework import status, views, permissions, decorators
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.views import JSONWebTokenAPIView
from rest_framework_jwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserCreateSerializer

# Create your views here.

User = get_user_model()

@decorators.api_view(['post'])
@decorators.permission_classes([permissions.AllowAny])
def registration(request):
    serializer = UserCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    user = serializer.save()
    refresh = RefreshToken.for_user(user)
    res = {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
    return Response(res, status.HTTP_201_CREATED)

# user auth
class UserLoginAPIView(JSONWebTokenAPIView):
    serializer_class = JSONWebTokenSerializer


class UserLogoutAPIView(views.APIView):
    permission_classes = {IsAuthenticated}

    def get(self, request, *args, **kwargs):
        user = request.user
        user.user_secret = uuid.uuid4()
        user.save()
        return Response({'detail': 'login out.', 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)


def get_user_secret(user):
    return user.user_secret

