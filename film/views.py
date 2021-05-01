from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from film.models import *
from .serializer import SupportSerializer
from rest_framework import viewsets

# -- html 페이지 주소 연동해 주는 곳 -----------

# index/ 메인 / film
def index(request):
    return render(request,'film/index.html')

# 커뮤니티
def community(request):
    return render(request,'film/community/community.html')\

# 영화 리뷰 모아 놓은 페이지
def movie_review_total(request):
    return render(request,'film/community/movie_review/movie_review_total.html')

# 영화 리뷰 상세 페이지
def movie_review_detail(request):
    return render(request,'film/community/movie_review/movie_review_detail.html')

# 영화 리뷰 작성 페이지
def movie_review_post(request):
    return render(request, 'film/community/movie_review/movie_review_post.html')

# 자유게시판 토탈 페이지
def free_board_total(request):
    return render(request, 'film/community/free_board/free_board_total.html')

# 자유게시판 상세 페이지
def free_board_detail(request):
    return render(request, 'film/community/free_board/free_board_detail.html')

# 자유게시판 작성 페이지
def free_board_post(request):
    return render(request, 'film/community/free_board/free_board_post.html')

# 배우 구인공고 토탈 페이지
def hire_actor_total(request):
    return render(request,'film/hire/actor/actor_total.html')

# 배우 구인공고 상세 페이지
def hire_actor_detail(request):
    return render(request,'film/hire/actor/actor_detail.html')

# 배우 구인공고 작성 페이지
def hire_actor_post(request):
    return render(request,'film/hire/actor/actor_post.html')

# 스탭 구인공고 total
def hire_staff_total(request):
    return render(request,'film/hire/staff/staff_total.html')

# 스텝 구인공고 상세 페이지
def hire_staff_detail(request):
    return render(request,'film/hire/staff/staff_detail.html')

# 스텝 구인공고 작성 페이지
def hire_staff_post(request):
    return render(request,'film/hire/staff/staff_post.html')


# 고객센터 페이지

class SupportViewSet(viewsets.ModelViewSet):
    queryset = Support.objects.all()
    serializer_class =SupportSerializer

def review(request):
    film_newest = Film.objects.all().order_by('-created_at')
    film_list = Film.objects.all().order_by('like_user_set')

    return render(request, 'film/film_list.html', {
        "film_list": film_list,
        "flim_newset" : film_newest,
    })