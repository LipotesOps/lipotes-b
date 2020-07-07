from django.urls import path
# jwt内部实现的登陆视图
from rest_framework_jwt.views import obtain_jwt_token
from . import views

urlpatterns=[
    path(r"login", views.UserLoginAPIView.as_view()),
    path(r"logout", views.UserLogoutAPIView.as_view()),
]