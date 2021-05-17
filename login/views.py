from django.shortcuts import render

# Create your views here.
# views.py
from django.shortcuts import redirect
import urllib


# code 요청
def kakao_login(request):
    app_rest_api_key = '5a366d7cd6acbacfd0e05e29e98a031e'

    redirect_uri = "http://127.0.0.1:8000/account/login/kakao/callback"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={app_rest_api_key}&redirect_uri={redirect_uri}&response_type=code"
    )


# access token 요청
def kakao_callback(request):
    params = urllib.parse.urlencode(request.GET)
    return redirect(f'https://kauth.kakao.com/oauth/token?{params}')