
from django.urls import path, include
from rest_auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from rest_auth.registration.views import RegisterView
from rest_framework.routers import DefaultRouter

from .views import KakaoToDjangoLogin, ChangePasswordView, ProfileViewSet

app_name = 'login'

router = DefaultRouter()
router.register('profile',ProfileViewSet)
urlpatterns = [
    path(r'',include(router.urls)),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    # path('rest-auth/kakao/', include('rest_auth.registration.urls')),

    # 회원가입
    # path('rest-auth/registration', RegisterView.as_view(), name='rest_register'),
    path('kakao/todjango/', KakaoToDjangoLogin.as_view(), name='kakao_todjango_login'),
    path('ChangePassword/', ChangePasswordView.as_view(), name='ChangePassword'),

]
