import uuid

from django.shortcuts import render

from rest_framework import status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.views import JSONWebTokenAPIView
from rest_framework_jwt.settings import api_settings

# Create your views here.

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