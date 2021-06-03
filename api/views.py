from django.http import HttpResponse
from django.shortcuts import redirect
from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
# from .models import FilmList
# Create your views here.
def HelloAPI(request):
    request.session['jwt'] = "123jwt"
    return HttpResponse(request.session.get('jwt'))
def Home(request):
    user = request.session.get('user')
    return redirect('http://localhost:8080')
# class FilmViewSet(viewsets.ModelViewSet):
#     queryset = FilmList.objects.all()
#     serializer_class = FilmSerializer

    # 작성자 들어갈때 들어갈 내용
    # def perform_create(self, serializer):
    #     serializer.save(user = self.request.user)