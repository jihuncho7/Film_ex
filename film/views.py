from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import AllowAny

from film.models import *
from .serializer import *
from rest_framework import viewsets
# 고객센터 페이지

class FilmViewSet(viewsets.ModelViewSet):
    queryset = Film.objects.all()
    serializer_class =FilmSerializer
    permission_classes = [AllowAny]
