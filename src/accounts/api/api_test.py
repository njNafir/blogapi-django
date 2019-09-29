"""
# api authentication test with rest_framework_simplejwt

pip install djangorestframework_simplejwt

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

pip install httpie

http post http://127.0.0.1:8000/api/token/simplejwt/ username=username password=password

{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTY5MzExNTc4LCJqdGkiOiJiNmNhYzBlNmJiMGM0NGI1YTk1ODQ2N2ZmNWNmMGFiNCIsInVzZXJfaWQiOjF9.PEupB_shtU4q4Q8mR7_zNmhdCqDLDsYFFuXDBZ9Mke0",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTU2OTM5NzY3OCwianRpIjoiOGEyNzBkZjc2NzdlNDJjMThmN2RlMWQwN2Y4ZGZhNTEiLCJ1c2VyX2lkIjoxfQ.8Q_ur3stFILqvLeWv_aZwmeR5n3UfnoZ4p3u4FF8Wpg"
}

http http://127.0.0.1:8000/hello/ "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTY5MzExNTc4LCJqdGkiOiJiNmNhYzBlNmJiMGM0NGI1YTk1ODQ2N2ZmNWNmMGFiNCIsInVzZXJfaWQiOjF9.PEupB_shtU4q4Q8mR7_zNmhdCqDLDsYFFuXDBZ9Mke0"

http post http://127.0.0.1:8000/api/token/simplejwt/refresh/ refresh=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTU2OTM5NzY3OCwianRpIjoiOGEyNzBkZjc2NzdlNDJjMThmN2RlMWQwN2Y4ZGZhNTEiLCJ1c2VyX2lkIjoxfQ.8Q_ur3stFILqvLeWv_aZwmeR5n3UfnoZ4p3u4FF8Wpg




# api authentication test with rest_framework_jwt

pip install djangorestframework-jwt


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}


from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

re_path(r'^api/token/jwt/', obtain_jwt_token, name='obtain_jwt_token'),
re_path(r'^api/token/jwt/refresh/', refresh_jwt_token, name='refresh_jwt_token'),



curl -X POST -d "username=username&password=password" http://127.0.0.1:8000/api/token/jwt/

{"token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo4LCJ1c2VybmFtZSI6ImFrIiwiZXhwIjoxNTY5MzE0NDU1LCJlbWFpbCI6ImFrQGdtYWlsLmNvbSJ9.wI91Yn4H28vnhbXyluTW_YDveVplEYO7a6bBjg1BDPc"}



curl -X POST -H "Content-Type: application/json" -d '{"username":"username","password":"password"}' http://127.0.0.1:8000/api/token/jwt/



curl -H "Authorization: JWT <your_token>" http://127.0.0.1:8000/protected-url/

curl -H "Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo4LCJ1c2VybmFtZSI6ImFrIiwiZXhwIjoxNTY5MzE0NDU1LCJlbWFpbCI6ImFrQGdtYWlsLmNvbSJ9.wI91Yn4H28vnhbXyluTW_YDveVplEYO7a6bBjg1BDPc" http://127.0.0.1:8000/comments/



curl -X POST -H "Content-Type: application/json" -d '{"token":"<EXISTING_TOKEN>"}' http://127.0.0.1:8000/api/token/jwt/refresh/

curl -X POST -H "Content-Type: application/json" -d '{"token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo4LCJ1c2VybmFtZSI6ImFrIiwiZXhwIjoxNTY5MzE0NDU1LCJlbWFpbCI6ImFrQGdtYWlsLmNvbSJ9.wI91Yn4H28vnhbXyluTW_YDveVplEYO7a6bBjg1BDPc"}' http://127.0.0.1:8000/api/token/jwt/refresh/

"""