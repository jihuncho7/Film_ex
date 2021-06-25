from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_auth.registration.views import SocialLoginView, SocialAccountListView
from rest_framework import generics
from .models import User
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import ReadOnlyModelViewSet
from allauth.socialaccount.providers.kakao import views as kakao_views
from allauth.socialaccount.providers.naver import views as naver_views
from allauth.socialaccount.providers.google import views as google_views
from rest_framework.permissions import IsAuthenticated

class KakaoToDjangoLogin(SocialLoginView):
    adapter_class = kakao_views.KakaoOAuth2Adapter
    client_class = OAuth2Client
    callback_url = 'localhost:8080'

class NaverToDjangoLogin(SocialLoginView):
    adapter_class = naver_views.NaverOAuth2Adapter
    client_class = OAuth2Client
    callback_url = 'localhost:8080'


class GoogleToDjangoLogin(SocialLoginView):
    adapter_class = google_views.GoogleOAuth2Adapter
    client_class = OAuth2Client
    callback_url = 'localhost:8080'
