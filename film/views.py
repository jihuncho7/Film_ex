from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import *
from .serializer import *
from rest_framework import viewsets
from itertools import chain # 쿼리셋 append 용
from rest_framework import filters
from django.db.models import Count


### Film Review

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 1000


# 고객센터 페이지
class FilmOrderbyRateViewSet(viewsets.ModelViewSet):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
    permission_classes = [AllowAny]  # FIXME 인증 구현해야함

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)

    global how_many_per_view  # obj 보내는 개수
    how_many_per_view = 15

    def get_queryset(self):  # 영화 평점 높은순 처리 로직
        qs = super().get_queryset()
        arr = []
        objpk = []

        obj = Film.objects.all()
        for o in obj:
            arr.append([o.get_rate(), o.pk])

        arr.sort(reverse=True)
        for i in range(how_many_per_view - 1):
            try:
                objpk.append(arr[i][1])
            except:
                pass
        objpk_list = list(objpk)
        qs = Film.objects.filter(pk__in=objpk_list)
        return qs


class FilmEditorChoiceViewSet(viewsets.ModelViewSet):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
    permission_classes = [AllowAny]  # FIXME 인증 구현해야함

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)

    def get_queryset(self):  # 영화 에디터 픽순
        qs = super().get_queryset()
        qs = qs.filter(is_picked=True)
        inner_q = qs.order_by('-created_at')[:how_many_per_view]
        inner_q_list = list(inner_q)
        qs = qs.filter(pk__in=inner_q_list)
        return qs


class FilmOnStreamingViewSet(viewsets.ModelViewSet):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
    permission_classes = [AllowAny]  # FIXME 인증 구현해야함

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)

    def get_queryset(self):  # 영화 에디터 픽순
        qs = super().get_queryset()
        qs = qs.filter(on_streaming=True)
        inner_q = qs.order_by('-created_at')[:how_many_per_view]
        inner_q_list = list(inner_q)
        qs = qs.filter(pk__in=inner_q_list)
        return qs


### FreeBoard

class FreeBoardViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    queryset = FreeBoard.objects.all()
    serializer_class = FreeBoardSerializer
    permission_classes = [IsAuthenticated]  # FIXME 인증 구현해야함
    # permission_classes = [AllowAny]  # FIXME 인증 구현해야함
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter,]
    search_fields = ['title', 'category', 'context']
    ordering_fields = ['num_like']
    ordering = ['-num_like', '-created_at']

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)


    # def perform_create(self, serializer):
    #
    #     serializer.save(author=self.request.user)
    #     return super().perform_create(serializer)

    def get_queryset(self):  # 추천 상위 5개 올리기
        qs = super().get_queryset()
        qs = qs.annotate(num_like=Count('like_user_set'))
        a = qs.filter(num_like__gte=2)[:5]
        a_list = list(a)
        b = qs.filter(num_like__lt=2).exclude(pk__in=a_list)
        c = list(chain(a, b))
        qs = qs.filter(pk__in=c)
        return qs


class HirePostStaffViewSet(viewsets.ModelViewSet):
    queryset = HirePostStaff.objects.all()
    serializer_class = HirePostStaffSerializer
    permission_classes = [AllowAny]  # FIXME 인증 구현해야함
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)

    def get_queryset(self): # 신규 상위 5개 올리기
        qs = super().get_queryset()
        a = qs.exclude(image='')[:5]
        b = qs.exclude(pk__in=a)
        c = list(chain(a, b))
        qs = qs.filter(pk__in=c)
        return qs


class HirePostActorViewSet(viewsets.ModelViewSet):
    queryset = HirePostActor.objects.all()
    serializer_class = HirePostActorSerializer
    permission_classes = [AllowAny]  # FIXME 인증 구현해야함
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)


class ResumeStaffViewSet(viewsets.ModelViewSet):
    queryset = ResumeStaff.objects.all()
    serializer_class = ResumeStaffSerializer
    permission_classes = [AllowAny]  # FIXME 인증 구현해야함

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)


class ResumeActorViewSet(viewsets.ModelViewSet):
    queryset = ResumeActor.objects.all()
    serializer_class = ResumeActorSerializer
    permission_classes = [AllowAny]  # FIXME 인증 구현해야함

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)


class QnAViewSet(viewsets.ModelViewSet):
    queryset = QnA.objects.all()
    serializer_class = QnASerializer
    permission_classes = [AllowAny]  # FIXME 인증 구현해야함

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)

