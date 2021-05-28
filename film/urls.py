from django.urls import path, include
from django.views.generic import TemplateView
from film import views
from .views import *
from rest_framework import routers
# -- Film의 view 와 멥핑해 주는 곳 -----------------

app_name = 'film'

router = routers.DefaultRouter()
# film review
router.register('FilmOrderbyRate',FilmOrderbyRateViewSet)
router.register('FilmEditorChoice',FilmEditorChoiceViewSet)
router.register('FilmOnStreaming',FilmOnStreamingViewSet)
# freeboard
router.register('freeboard',FreeBoardViewSet)
# hire post
router.register('hirepoststaff',HirePostStaffViewSet)
router.register('hirepostactor',HirePostActorViewSet)
# Resume
router.register('resumestaff',ResumeStaffViewSet)
router.register('resumeactor',ResumeActorViewSet)
# QnA
router.register('qna',QnAViewSet)
urlpatterns = [
    path(r'',include(router.urls)),

    #path('review/', views.review, name='review'),
]
