"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls.static import static
from django.conf import settings

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from accounts.views import (login_view, register_view, logout_view)

urlpatterns = [
    
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^comments/', include("comments.urls")),
    
    re_path(r'^register/', register_view, name='register'),
    re_path(r'^login/', login_view, name='login'),
    re_path(r'^logout/', logout_view, name='logout'),
    re_path(r'^', include("posts.urls")),
    re_path(r'^api/posts/', include("posts.api.urls")),
    re_path(r'^api/comments/', include("comments.api.urls")),
    re_path(r'^api/users/', include("accounts.api.urls")),

    # api authentication test with rest_framework_simplejwt
    re_path(r'^api/token/simplejwt/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    re_path(r'^api/token/simplejwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # api authentication test with rest_framework_jwt
    re_path(r'^api/token/jwt/', obtain_jwt_token, name='obtain_jwt_token'),
    re_path(r'^api/token/jwt/refresh/', refresh_jwt_token, name='refresh_jwt_token'),

    #url(r'^posts/$', "<appname>.views.<function_name>"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)