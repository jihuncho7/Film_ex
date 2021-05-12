from django.urls import path, include
from django.views.generic import TemplateView
from film import views
from .views import *
from rest_framework import routers
# -- Film의 view 와 멥핑해 주는 곳 -----------------

app_name = 'film'

router = routers.DefaultRouter()
router.register(r'FilmOrderbyRate',FilmOrderbyRateViewSet)
router.register(r'FilmEditorChoice',FilmEditorChoiceViewSet)
router.register(r'FilmOnStreaming',FilmOnStreamingViewSet)
urlpatterns = [
    path(r'',include(router.urls)),
    #path('review/', views.review, name='review'),
]
