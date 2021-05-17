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

class CommentSerializer(serializers.ModelSerializer):
    # user = serializers.ReadOnlyField(source='user.nickname')
    class Meta:
        model = Comment
        fields = '__all__'

class FreeBoardSerializer(serializers.ModelSerializer):
    # user = serializers.ReadOnlyField(source='user.nickname')
    get_likes = serializers.SerializerMethodField()
    # is_like_user = serializers.SerializerMethodField() todo 유저 글쓴이 여부
    def get_get_likes(self, instance):
        return instance.get_likes()
    # def get_is_like_user(self, instance): todo 유저 글쓴이 여부
    #     return instance.is_like_user()

    class Meta:
        model = FreeBoard
        fields = ('id','hit','author','get_likes','created_at',
                  'updated_at','title','context','image',
                  )
        read_only_fields = ('hit','author','like_user_set')

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



