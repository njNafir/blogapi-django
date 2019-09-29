from django.urls import path, re_path
from django.contrib import admin

from .views import (
	UserCreateAPIView,
	UserLoginAPIView
    )

urlpatterns = [
    re_path(r'^login/$', UserLoginAPIView.as_view(), name='login_api'),
    re_path(r'^register/$', UserCreateAPIView.as_view(), name='register_api'),
]
