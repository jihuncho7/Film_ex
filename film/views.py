import django_filters
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_haystack.viewsets import HaystackViewSet
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db.models import Case, When, Q
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializer import *
from rest_framework import viewsets, status
from itertools import chain # 쿼리셋 append 용
from rest_framework import filters
from django.db.models import Count

### Film Review

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 1000



"""
게시판 뷰
"""

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
        preserved = Case(*[When(pk=pk, then=pos) for pos,pk in enumerate(objpk)])
        qs = Film.objects.filter(pk__in=objpk_list)
        qs = qs.order_by(preserved, '-created_at')
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
    queryset = FreeBoard.objects.all()
    serializer_class = FreeBoardSerializer
    permission_classes = [AllowAny]  # FIXME 인증 구현해야함
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter,filters.SearchFilter]
    filterset_fields = [ 'category' ]
    search_fields = ['title','context']
    # ordering = ['-num_like', '-created_at']

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)

    # def perform_update(self, serializer):
    #     try:
    #         if self.request.data['like_id']:
    #             data = self.get_object().like_user_set.all()
    #             user_id = self.request.user.pk
    #             if data.filter(id=user_id):
    #                 self.get_object().like_user_set.remove(user_id)
    #             else:
    #                 self.get_object().like_user_set.add(str(user_id))
    #     except ObjectDoesNotExist:
    #         print('추천을 위한 PATCH는 작동하지 않았음')
    @action(detail=True, methods=['POST'])
    def like(self, request, pk):
        post = self.get_object()
        post.like_user_set.add(self.request.user.pk)
        return Response(status.HTTP_201_CREATED)

    @like.mapping.delete
    def unlike(self,request, pk):
        post = self.get_object()
        post.like_user_set.remove(self.request.user.pk)
        return Response(status.HTTP_204_NO_CONTENT)

 #TODO 할차례 0607 참조


    # def perform_create(self, serializer):
    #
    #     serializer.save(author=self.request.user)
    #     return super().perform_create(serializer)

    def get_queryset(self):  # 추천 상위 5개 올리기 TODO 추천 기준 2개에서 5개로 올리기
        qs = super().get_queryset()
        qs = qs.annotate(num_like=Count('like_user_set'))
        a = qs.filter(num_like__gte=2).order_by('-num_like')[:5]
        a_list = list(a)
        b = qs.filter(num_like__lt=2).order_by('-created_at').exclude(pk__in=a_list)
        c = list(chain(a, b))
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(c)])
        qs = qs.filter(pk__in=c).order_by(preserved)
        return qs


class HirePostStaffViewSet(viewsets.ModelViewSet):
    queryset = HirePostStaff.objects.all()
    serializer_class = HirePostStaffSerializer
    permission_classes = [AllowAny]  # FIXME 인증 구현해야함
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['category']
    search_fields = ['title', 'context']

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)

    def get_queryset(self): # 신규 상위 5개 올리기
        qs = super().get_queryset()
        a = qs.filter(image='')[:5]
        a_list = list(a)
        b = qs.exclude(pk__in=a_list)
        c = list(chain(a, b))
        qs = qs.filter(pk__in=c)
        return qs

    @action(detail=True, methods=['POST'])
    def like(self, request, pk):
        post = self.get_object()
        post.like_user_set.add(self.request.user.pk)
        return Response(status.HTTP_201_CREATED)

    @like.mapping.delete
    def unlike(self,request, pk):
        post = self.get_object()
        post.like_user_set.remove(self.request.user.pk)
        return Response(status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['POST'])
    def apply(self, request, pk):
        post = self.get_object()
        post.is_applied_set.add(self.request.user.pk)
        return Response(status.HTTP_201_CREATED)

    @apply.mapping.delete
    def unapply(self,request, pk):
        post = self.get_object()
        post.is_applied_set.remove(self.request.user.pk)
        return Response(status.HTTP_204_NO_CONTENT)

class HirePostActorViewSet(viewsets.ModelViewSet):
    queryset = HirePostActor.objects.all()
    serializer_class = HirePostActorSerializer
    permission_classes = [AllowAny]  # FIXME 인증 구현해야함
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['category']
    search_fields = ['title', 'context']

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)

    @action(detail=True, methods=['POST'])
    def like(self, request, pk):
        post = self.get_object()
        post.like_user_set.add(self.request.user.pk)
        return Response(status.HTTP_201_CREATED)

    @like.mapping.delete
    def unlike(self,request, pk):
        post = self.get_object()
        post.like_user_set.remove(self.request.user.pk)
        return Response(status.HTTP_204_NO_CONTENT)


class ResumeStaffViewSet(viewsets.ModelViewSet):
    queryset = ResumeStaff.objects.all()
    serializer_class = ResumeStaffSerializer
    permission_classes = [AllowAny]  # FIXME 인증 구현해야함
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, ]
    search_fields = ['title', 'author_username', 'context']

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(author=self.request.user.pk)
        return qs

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)


class ResumeActorViewSet(viewsets.ModelViewSet):
    queryset = ResumeActor.objects.all()
    serializer_class = ResumeActorSerializer
    permission_classes = [AllowAny]  # FIXME 인증 구현해야함
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, ]
    search_fields = ['title', 'author_username', 'context']

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(author=self.request.user.pk)
        return qs

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


"""

기능적인 뷰들

"""
class ResumeStaffBoard(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = ResumeStaffSerializer
    queryset = ResumeStaff.objects.all()

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)

    def get_queryset(self): # 인기순 15개 이미지 존재하는 포스트 필터
        qs = super().get_queryset()
        qs = qs.filter(is_publish=True)
        return qs

class ResumeActorBoard(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = ResumeActorSerializer
    queryset = ResumeActor.objects.all()
    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)

    def get_queryset(self): # 인기순 15개 이미지 존재하는 포스트 필터
        qs = super().get_queryset()
        qs = qs.filter(is_publish=True)
        return qs

class Home_banner(APIView):
    permission_classes = [AllowAny]

    def get(self, request):

        qs = Film.objects.filter(is_picked=True)[:2]
        qs2 = FreeBoard.objects.all().order_by('-created_at')[:2]
        a = FilmSerializer(qs, many=True,fields=('title', 'id'))
        b = FreeBoardSerializer(qs2, many=True,fields=('title', 'id'))
        return Response(a.data+b.data)

class HirePostStaff_imgfilter(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = HirePostStaffSerializer
    queryset = HirePostStaff.objects.all()

    def get_queryset(self): # 인기순 15개 이미지 존재하는 포스트 필터
        qs = super().get_queryset()
        qs = qs.exclude(image='')
        qs = qs.order_by('-like_user_set')[:15]
        return qs


class MypageApplied(APIView):
    permission_classes = [AllowAny]

    def get(self, request):

        qs = HirePostStaff.objects.filter(is_applied_set=self.request.user.pk)
        qs2 = HirePostActor.objects.filter(is_applied_set=self.request.user.pk)
        a = MyHirePostStaffSerializer(qs,many=True)
        b = MyHirePostActorSerializer(qs2, many=True)
        return Response(a.data+b.data)


class WrittenByMe(APIView):
    permission_classes = [AllowAny]

    def get(self, request):

        qs = Film.objects.filter(author=self.request.user.pk)
        qs2 = FreeBoard.objects.filter(author=self.request.user.pk)
        qs3 = HirePostStaff.objects.filter(author=self.request.user.pk)
        qs4 = HirePostActor.objects.filter(author=self.request.user.pk)
        s1 = FilmSerializer(qs,many=True,fields=('id','hit','title','created_at','postfrom'))
        s2 = FreeBoardSerializer(qs2, many=True,fields=('id','hit','title','created_at','postfrom'))
        s3 = HirePostStaffSerializer(qs3, many=True,fields=('id','hit','title','created_at','postfrom'))
        s4 = HirePostActorSerializer(qs4, many=True,fields=('id','hit','title','created_at','postfrom'))
        return Response(s1.data+s2.data+s3.data+s4.data)

class CountLikedPost(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        q_like = HirePostStaff.objects.filter(like_user_set=self.request.user.pk).count()
        q_like2 = HirePostActor.objects.filter(like_user_set=self.request.user.pk).count()
        q_applied = HirePostStaff.objects.filter(is_applied_set=self.request.user.pk).count()
        q_applied2 = HirePostActor.objects.filter(is_applied_set=self.request.user.pk).count()
        q_resume = ResumeStaff.objects.filter(author=self.request.user.pk)
        q_resume2 = ResumeActor.objects.filter(author=self.request.user.pk)
        arr = 0
        for i in q_resume:
            arr+i.hit
        for i in q_resume2:
            arr+i.hit
        return Response({"likes": q_like + q_like2,
                         "applied":q_applied+q_applied2,
                         "resumes_hit":arr,
                         })

class CountAllPost(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        q = Film.objects.filter(author=self.request.user.pk).count()
        q1 = FreeBoard.objects.filter(author=self.request.user.pk).count()
        q2 = HirePostStaff.objects.filter(author=self.request.user.pk).count()
        q3 = HirePostActor.objects.filter(author=self.request.user.pk).count()
        q4 = ResumeStaff.objects.filter(author=self.request.user.pk).count()
        q5 = ResumeActor.objects.filter(author=self.request.user.pk).count()
        counts = q+q1+q2+q3+q4+q5
        c1 = Comment.objects.filter(author=self.request.user.pk).count()
        c2 = CommentFreeBoard.objects.filter(author=self.request.user.pk).count()
        c3 = CommentHirePostStaff.objects.filter(author=self.request.user.pk).count()
        c4 = CommentHirePostActor.objects.filter(author=self.request.user.pk).count()
        comments = c1+c2+c3+c4
        return Response({"posts": counts,
                         "comments": comments,
                         })

# class SearchAll(viewsets.ModelViewSet):
#     permission_classes = [AllowAny]
#     filter_backends = [filters.SearchFilter, filters.OrderingFilter, ]
#     search_fields = ['title']
#     serializer_class = FreeBoardSerializer
#
#     def get(self, request):
#         q = Film.objects.all()
#         q1 = FreeBoard.objects.all()
#         q2 = HirePostStaff.objects.all()
#         q3 = HirePostActor.objects.all()
#         s1 = FilmSerializer(q,many=True,fields=('id','hit','title','created_at','postfrom'))
#         s2 = FreeBoardSerializer(q1, many=True,fields=('id','hit','title','created_at','postfrom'))
#         s3 = HirePostStaffSerializer(q2, many=True,fields=('id','hit','title','created_at','postfrom'))
#         s4 = HirePostActorSerializer(q3, many=True,fields=('id','hit','title','created_at','postfrom'))
#
#         return Response({"film": s1.data,
#                          "freeboard": s2.data,
#                          "hirepoststaff": s3.data,
#                          "hirepostactor": s4.data,
#                          })


"""

코멘트 뷰

"""

class CommentViewset(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]  # FIXME 인증 구현해야함

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)

class CommentInCommmentViewset(viewsets.ModelViewSet):
    queryset = CommentInComment.objects.all()
    serializer_class = CommentInCommentSerializer
    permission_classes = [AllowAny]  # FIXME 인증 구현해야함

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)

class CommentFreeBoardViewset(viewsets.ModelViewSet):
    queryset = CommentFreeBoard.objects.all()
    serializer_class = CommentFreeBoardSerializer
    permission_classes = [AllowAny]  # FIXME 인증 구현해야함

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)

class CommentInCommmentFreeBoardViewset(viewsets.ModelViewSet):
    queryset = CommentFreeBoard.objects.all()
    serializer_class = CommentInCommentFreeBoardSerializer
    permission_classes = [AllowAny]  # FIXME 인증 구현해야함

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)

class CommentHirePostStaffViewset(viewsets.ModelViewSet):
    queryset = CommentHirePostStaff.objects.all()
    serializer_class = CommentHirePostStaffSerializer
    permission_classes = [AllowAny]  # FIXME 인증 구현해야함

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)

class CommentInCommentHirePostStaffViewset(viewsets.ModelViewSet):
    queryset = CommentInCommentHirePostStaff.objects.all()
    serializer_class = CommentInCommentHirePostStaffSerializer
    permission_classes = [AllowAny]  # FIXME 인증 구현해야함

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)

class CommentHirePostActorViewset(viewsets.ModelViewSet):
    queryset = CommentHirePostActor.objects.all()
    serializer_class = CommentHirePostActorSerializer
    permission_classes = [AllowAny]  # FIXME 인증 구현해야함

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)

class CommentInCommentHirePostActorViewset(viewsets.ModelViewSet):
    queryset = CommentInCommentHirePostActor.objects.all()
    serializer_class = CommentInCommentHirePostActorSerializer
    permission_classes = [AllowAny]  # FIXME 인증 구현해야함

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(author=author)

from rest_framework.response import Response
from rest_framework.views import APIView

class SearchAllView(APIView):

    permission_classes = [AllowAny]

    def post(self, request, format=None):
        query = request.data
        or_lookup = (Q(context__icontains=query) |
                     Q(title__icontains=query)
                     )
        qs = ResumeStaff.objects.filter(or_lookup)
        qs2 = FreeBoard.objects.filter(or_lookup)
        rq = ResumeStaffSerializer(qs,many=True)
        rq2 = FreeBoard_SubSerializer(qs2,many=True)

        return Response({
                         "freeboard": rq2.data,
                         "resumestaff": rq.data,

                        })