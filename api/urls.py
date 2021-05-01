# api/urls.py

from django.urls import path, include

from rest_framework import routers
from rest_framework.routers import DefaultRouter


app_name = 'api'

router = routers.DefaultRouter()


urlpatterns = [
    # path("hello/", HelloAPI),

    path('',include(router.urls)),

]

