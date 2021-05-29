# api/urls.py

from django.urls import path, include

from rest_framework import routers
from rest_framework.routers import DefaultRouter

from api.views import HelloAPI, Home

app_name = 'api'

router = routers.DefaultRouter()


urlpatterns = [
    path("hello/", HelloAPI),
    path("home/", Home),

    path('',include(router.urls)),

]

