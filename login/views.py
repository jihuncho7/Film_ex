from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_auth.registration.views import SocialLoginView

from allauth.socialaccount.providers.kakao import views as kakao_views
from rest_framework import status
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializer import ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated


class KakaoToDjangoLogin(SocialLoginView):
    adapter_class = kakao_views.KakaoOAuth2Adapter
    client_class = OAuth2Client
    callback_url = 'localhost:8080'


class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["이전 비밀번호가 틀렸습니다."]}, status=status.HTTP_400_BAD_REQUEST)
            if not serializer.data.get("new_password") == serializer.data.get("new_password_2"):
                return Response({"new_password": ["동일한 새 비밀번호를 입력하세요."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
