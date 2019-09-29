from django.urls import path, re_path
from django.contrib import admin

from .views import (
	PostCreateAPIView,
	PostDeleteAPIView,
	PostDetailAPIView,
	PostListAPIView,
	PostUpdateAPIView
	)

urlpatterns = [
	re_path(r'^$', PostListAPIView.as_view(), name='list_api'),
    re_path(r'^create/$', PostCreateAPIView.as_view(), name='create_api'),
    re_path(r'^(?P<slug>[\w-]+)/$', PostDetailAPIView.as_view(), name='detail_api'),
    re_path(r'^(?P<slug>[\w-]+)/edit/$', PostUpdateAPIView.as_view(), name='update_api'),
    re_path(r'^(?P<slug>[\w-]+)/delete/$', PostDeleteAPIView.as_view(), name='delete_api'),
]
