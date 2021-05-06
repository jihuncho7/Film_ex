from django.urls import path, include
from django.views.generic import TemplateView
from film import views
from .views import *
from rest_framework import routers

from rest_framework.routers import DefaultRouter
# -- Film의 view 와 멥핑해 주는 곳 -----------------

app_name = 'film'

router = routers.DefaultRouter()
router.register('support',SupportViewSet)

urlpatterns = [
    path('community/',community),
    path('mv_rv_total/',movie_review_total),
    path('mv_rv_detail/', movie_review_detail),
    path('mv_rv_post/', movie_review_post),
    path('free_board_total/', free_board_total),
    path('free_board_detail/', free_board_detail),
    path('free_board_post/', free_board_post),

    path('hire_actor_total/', hire_actor_total),
    path('hire_actor_detail/', hire_actor_detail),
    path('hire_actor_post/', hire_actor_post),

    path('hire_staff_total/', hire_staff_total),
    path('hire_staff_detail/', hire_staff_detail),
    path('hire_staff_post/', hire_staff_post),

    path('',include(router.urls)),

    path('review/', views.review, name='review'),
]
