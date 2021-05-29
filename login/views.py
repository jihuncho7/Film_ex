from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_auth.registration.views import SocialLoginView, SocialAccountListView

from allauth.socialaccount.providers.kakao import views as kakao_views


class KakaoToDjangoLogin(SocialLoginView):
    adapter_class = kakao_views.KakaoOAuth2Adapter
    client_class = OAuth2Client
    callback_url = 'localhost:8080'


class SocialList(SocialAccountListView):
    pass

