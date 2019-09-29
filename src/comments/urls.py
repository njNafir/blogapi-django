from django.urls import path, re_path
from django.contrib import admin

from .views import (
    comment_thread,
    comment_delete

    )

urlpatterns = [
    re_path(r'^(?P<id>\d+)/$', comment_thread, name='thread'),
    re_path(r'^(?P<id>\d+)/delete/$', comment_delete, name='delete'),
]
