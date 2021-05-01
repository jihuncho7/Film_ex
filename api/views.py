from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .models import FilmList
from .serializers import FilmSerializer
# Create your views here.
@api_view(['GET'])
def HelloAPI(request):
    return Response("hello world!")

class FilmViewSet(viewsets.ModelViewSet):
    queryset = FilmList.objects.all()
    serializer_class = FilmSerializer

    # 작성자 들어갈때 들어갈 내용
    # def perform_create(self, serializer):
    #     serializer.save(user = self.request.user)