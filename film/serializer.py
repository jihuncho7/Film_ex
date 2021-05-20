

from .models import *
from rest_framework import serializers


read_only_fields_global = ('hit','author','like_user_set','tag_set')

class FilmSerializer(serializers.ModelSerializer):

    rate_show = serializers.SerializerMethodField()
    author_username = serializers.ReadOnlyField(source='author.username')


    def get_rate_show(self, instance):
        return instance.get_rate()
    class Meta:
        model = Film
        fields = '__all__'
        read_only_fields = read_only_fields_global

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('author','post')

class FreeBoardSerializer(serializers.ModelSerializer):
    # user = serializers.ReadOnlyField(source='user.nickname')
    get_likes = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    tag_set = serializers.StringRelatedField(many=True)
    author_username = serializers.ReadOnlyField(source='author.username')

    # is_like_user = serializers.SerializerMethodField() todo 유저 글쓴이 여부
    def get_get_likes(self, obj):
        return obj.get_likes()

    def get_category(self, obj):
        return obj.get_category_display()

    # def get_is_like_user(self, instance): todo 유저 글쓴이 여부
    #     return instance.is_like_user()
    class Meta:
        model = FreeBoard
        fields = ('id','hit','author_username','get_likes','created_at',
                  'updated_at','title','context','image','category',
                  'tag_set'
                  )
        read_only_fields = read_only_fields_global

class HirePostStaffSerializer(serializers.ModelSerializer):

    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = HirePostStaff
        fields = ('id','hit','author_username','thumbs','created_at',
                  'updated_at','title','context','image','category',
                  'tag_set','like_user_set','payment','requirement','advantage',
                  'job_loca','company','company_loca','company_desc','deadline',
                  'company_url','job_position'
                  )
        read_only_fields = read_only_fields_global

class HirePostActorSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = HirePostActor
        fields = '__all__'
        read_only_fields = read_only_fields_global

class ResumeStaffSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    class Meta:
        model = ResumeStaff
        fields = '__all__'

class ResumeActorSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    class Meta:
        model = ResumeActor
        fields = '__all__'

class QnASerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    class Meta:
        model = QnA
        fields = '__all__'



