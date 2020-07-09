from django.urls import path

from rest_framework_simplejwt import views as jwt_views
from . import views

urlpatterns=[
    path(r"login/", views.UserLoginAPIView.as_view()),
    path(r"logout/", views.UserLogoutAPIView.as_view()),
    path(r'register/', views.registration, name='register'),
    path(r'token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(r'token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh')
]