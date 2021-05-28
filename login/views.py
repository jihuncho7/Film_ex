import json

import jwt
from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect
import requests
from django.http import JsonResponse, HttpResponse
from allauth.socialaccount.providers.kakao import views as kakao_view
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_auth.registration.views import SocialLoginView
from rest_auth.registration.views import RegisterView
from rest_auth.views import LoginView
from allauth.socialaccount.models import SocialAccount
from djangoProject import settings
from .models import User
from allauth.socialaccount.providers.kakao import views as kakao_views

class KakaoException(Exception):
    pass


class KakaoLoginView(SocialLoginView):

    def get(self, request):
        REST_API_KEY = '445eccf206b046c8d5adf4bfba7b1e54'
        REDIRECT_URI = 'http://127.0.0.1:8000/login/kakao/callback'

        API_HOST = f'https://kauth.kakao.com/oauth/authorize?client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}&response_type=code'

        #API_HOST = f'https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}&code={CODE}'
        return redirect(API_HOST)

class KakaoCallbackView(View):
    def get(self, request):


        try:
            code = request.GET.get("code")
            print("code", code)

            REST_API_KEY = '445eccf206b046c8d5adf4bfba7b1e54'
            REDIRECT_URI = 'http://127.0.0.1:8000/login/kakao/callback'

            token_request = requests.get(
                f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}&code={code}"
            )
            token_json = token_request.json()
            error = token_json.get("error", None)

            # if there is an error from token_request
            if error is not None:
                return JsonResponse({"message": "INVALID_CODE"}, status=400)

            access_token = token_json.get('access_token')
            print("access_token", access_token)

            # # ------get kakaotalk profile info------#
            profile_request = requests.get(

                "https://kapi.kakao.com/v2/user/me", headers={"Authorization": f"Bearer {access_token}"},
            )

            profile_json = profile_request.json()

            # parsing profile json
            kakao_account = profile_json.get("kakao_account")
            email = kakao_account.get("email", None)

            if email is None:  # 이메일이 없으면 // 동의시 이메일 동의 해야 함
                raise KakaoException()  # 이메일은 비즈니스 채널이 아니면 필수 제공 x\

            profile = kakao_account.get("profile") # 닉네임, 프로필사진
            print(profile)

            print(email)
            nickname = profile.get("nickname")
            profile_image = profile.get("thumbnail_image_url") # 사이즈 설정
            print('image', profile_image)
            print(code)
            print(access_token)

            if User.objects.filter(email = email).exists(): # 접속한 이메일이 DB에 있나 확인
                user = User.objects.get(email = email) # 있으면 그 객체를 가져옴 #id로 할거면 바꾸면 됨~~
                token = jwt.encode({"email":email}, settings.SECRET_KEY, algorithm ="HS256") # 이메일 정보로 토큰발핼
                token = token.decode("utf-8")

                # self.request.session['token'] = token
                req =redirect(

                    f"http://localhost:8000/login/kakao/todjango?access_token={access_token}&code={code}")

                return req
            else: # 새로운 객체 만들기
                User(
                    email = email,
                    social = 'kakao',
                    username = nickname
                ).save()
                token = jwt.encode({"email":email}, settings.SECRET_KEY, algorithm="HS256")
                token = token.decode("utf-8")
                return redirect('http://localhost:8000/login/kakao/todjango/',data= {'access_token':access_token})

        except KakaoException:
            return redirect("/error")

class KakaoToDjangoLogin(SocialLoginView):
    adapter_class = kakao_views.KakaoOAuth2Adapter
    # client_class = OAuth2Client
    # callback_url = KAKAO_CALLBACK_URI
