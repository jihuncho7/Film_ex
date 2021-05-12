from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny

from .models import *
from .serializer import *
from rest_framework import viewsets

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 1000
# 고객센터 페이지
class FilmOrderbyRateViewSet(viewsets.ModelViewSet):
    queryset = Film.objects.all()
    serializer_class =FilmSerializer
    permission_classes = [AllowAny] #FIXME 인증 구현해야함
    pagination_class = StandardResultsSetPagination
    global how_many_per_view #  obj 보내는 개수
    how_many_per_view = 15
    def get_queryset(self): # 영화 평점 높은순 처리 로직
        qs = super().get_queryset()
        arr = []
        objpk = []

        obj = Film.objects.all()
        for o in obj:
            arr.append([o.get_rate(),o.pk])

        arr.sort(reverse=True)
        for i in range(how_many_per_view-1):
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
        inner_q = qs.order_by('-created_at')[:how_many_per_view]
        qs = qs.filter(pk__in=inner_q)
        return qs

class FilmOnStreamingViewSet(viewsets.ModelViewSet):
    queryset = Film.objects.all()
    serializer_class =FilmSerializer
    permission_classes = [AllowAny] #FIXME 인증 구현해야함

    def get_queryset(self): # 영화 에디터 픽순
        qs = super().get_queryset()
        qs = qs.filter(on_streaming=True)
        inner_q = qs.order_by('-created_at')[:how_many_per_view]
        qs = qs.filter(pk__in=inner_q)
        return qs