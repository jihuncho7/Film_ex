from .models import *
from rest_framework import serializers

class SupportSerializer(serializers.ModelSerializer):
    # user = serializers.ReadOnlyField(source='user.nickname')
    class Meta:
        model = Support
        fields = ['id', 'title', 'created_at', 'context']

class FilmSerializer(serializers.ModelSerializer):
    # user = serializers.ReadOnlyField(source='user.nickname')
    class Meta:
        model = Film
        fields = ['__all__']