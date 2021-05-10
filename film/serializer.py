from .models import *
from rest_framework import serializers

class FilmSerializer(serializers.ModelSerializer):
    # user = serializers.ReadOnlyField(source='user.nickname')
    rate_show = serializers.SerializerMethodField()

    def get_rate_show(self, instance):
        return instance.get_rate()
    class Meta:
        model = Film
        fields = '__all__'




class FreeBoardSerializer(serializers.ModelSerializer):
    # user = serializers.ReadOnlyField(source='user.nickname')
    class Meta:
        model = FreeBoard
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    # user = serializers.ReadOnlyField(source='user.nickname')
    class Meta:
        model = Comment
        fields = '__all__'

class FreeBoardSerializer(serializers.ModelSerializer):
    # user = serializers.ReadOnlyField(source='user.nickname')
    class Meta:
        model = FreeBoard
        fields = '__all__'

class HirePostStaffSerializer(serializers.ModelSerializer):
    # user = serializers.ReadOnlyField(source='user.nickname')
    class Meta:
        model = HirePostStaff
        fields = '__all__'

class HirePostActorSerializer(serializers.ModelSerializer):
    # user = serializers.ReadOnlyField(source='user.nickname')
    class Meta:
        model = HirePostActor
        fields = '__all__'

class ResumeStaffSerializer(serializers.ModelSerializer):
    # user = serializers.ReadOnlyField(source='user.nickname')
    class Meta:
        model = ResumeStaff
        fields = '__all__'

class ResumeActorSerializer(serializers.ModelSerializer):
    # user = serializers.ReadOnlyField(source='user.nickname')
    class Meta:
        model = ResumeActor
        fields = '__all__'

class QnASerializer(serializers.ModelSerializer):
    # user = serializers.ReadOnlyField(source='user.nickname')
    class Meta:
        model = QnA
        fields = '__all__'



