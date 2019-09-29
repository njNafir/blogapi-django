from django.urls import path, re_path
from django.contrib import admin

from .views import (
	CommentCreateAPIView,
    CommentListAPIView,
    CommentDetailAPIView,
    # CommentEditAPIView
    )

urlpatterns = [
    re_path(r'^$', CommentListAPIView.as_view(), name='thread_list_api'),
    re_path(r'^(?P<pk>\d+)/$', CommentDetailAPIView.as_view(), name='thread_detail_api'),
    re_path(r'^create/$', CommentCreateAPIView.as_view(), name='thread_create_api'),
    # re_path(r'^(?P<pk>\d+)/edit/$', CommentEditAPIView.as_view(), name='thread_edit_api'),
]
