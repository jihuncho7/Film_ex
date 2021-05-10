from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import AllowAny

from .models import *
from .serializer import *
from rest_framework import viewsets
# 고객센터 페이지

class FilmOrderbyRateViewSet(viewsets.ModelViewSet):
    queryset = Film.objects.all()
    serializer_class =FilmSerializer
    permission_classes = [AllowAny] #FIXME 인증 구현해야함

    def get_queryset(self): # 영화 평점 높은순 처리 로직
        qs = super().get_queryset()
        arr = []
        objpk = []
        obj = Film.objects.all()
        for o in obj:
            arr.append([o.get_rate(),o.pk])

        arr.sort(reverse=True)
        for i in range(14):
            try:
                objpk.append(arr[i][1])
            except:
                pass
        qs = Film.objects.filter(pk__in=objpk)
        return qs

class FilmEditorChoiceViewSet(viewsets.ModelViewSet):
    queryset = Film.objects.all()
    serializer_class =FilmSerializer
    permission_classes = [AllowAny] #FIXME 인증 구현해야함

    def get_queryset(self): # 영화 에디터 픽순
        qs = super().get_queryset()
        qs = qs.filter(is_picked=True)
        qs = qs.order_by('-created_at')[:15]
        return qs

class FilmOnStreamingViewSet(viewsets.ModelViewSet):
    queryset = Film.objects.all()
    serializer_class =FilmSerializer
    permission_classes = [AllowAny] #FIXME 인증 구현해야함

    def get_queryset(self): # 영화 에디터 픽순
        qs = super().get_queryset()
        qs = qs.filter(on_streaming=True)
        qs = qs.order_by('-created_at')[:15]
        return qs