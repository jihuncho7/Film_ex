
from django.urls import path, include
from rest_auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from rest_auth.registration.views import RegisterView
from .views import KakaoToDjangoLogin, SocialList

from film import views
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

# urlpatterns = [
#     path(r'api-jwt-auth/', obtain_jwt_token),          # JWT 토큰 획득
#     path(r'api-jwt-auth/refresh/', refresh_jwt_token), # JWT 토큰 갱신
#     path(r'api-jwt-auth/verify/', verify_jwt_token),   # JWT 토큰 확인
# ]

urlpatterns = [
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    # path('rest-auth/kakao/', include('rest_auth.registration.urls')),

    # 회원가입
    # path('rest-auth/registration', RegisterView.as_view(), name='rest_register'),
    path('kakao/todjango/', KakaoToDjangoLogin.as_view(), name='kakao_todjango_login'),
    path('sociallist/', SocialList.as_view(), name='sociallist'),

]
