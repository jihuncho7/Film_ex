

from .models import *
from rest_framework import serializers


read_only_fields_global = (['author'])

"""

코멘트 시리얼라이저

"""
class CommentInCommentFreeBoardSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = CommentInCommentFreeBoard
        fields = '__all__'
        read_only_fields = read_only_fields_global

class CommentFreeBoardSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    CommentInCommentFreeBoard = CommentInCommentFreeBoardSerializer(many=True,read_only=True)
    class Meta:
        model = CommentFreeBoard
        fields = '__all__'
        read_only_fields = read_only_fields_global



class FilmSerializer(serializers.ModelSerializer):

    rate_show = serializers.SerializerMethodField()
    author_username = serializers.ReadOnlyField(source='author.username')


    def get_rate_show(self, instance):
        return instance.get_rate()
    class Meta:
        model = Film
        fields = '__all__'
        read_only_fields = read_only_fields_global

    # views.py 에서 필드 수정 할 수 있게 하는 커스텀 쿼리
    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(FilmSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('author','post')

class FreeBoardSerializer(serializers.ModelSerializer, object):
    # user = serializers.ReadOnlyField(source='user.nickname')
    get_likes = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    tag_set = serializers.SerializerMethodField()
    author_username = serializers.ReadOnlyField(source='author.username')
    is_like_user = serializers.SerializerMethodField()
    CommentFreeBoard = CommentFreeBoardSerializer(many=True,read_only=True)

    def get_get_likes(self, obj):
        return obj.get_likes()

    def get_category(self, obj):
        return obj.get_category_display()

    def get_tag_set(self, obj):
        return obj.extract_tag_list()

    def get_is_like_user(self, instance):
        return instance.is_like_user(self.context['request'].user)

    class Meta:
        model = FreeBoard
        fields = ('id','hit','author_username','get_likes','created_at',
                  'updated_at','title','context','image','category',
                  'tag_set','is_like_user','like_user_set','CommentFreeBoard',
                  )
        read_only_fields = read_only_fields_global

    # views.py 에서 필드 수정 할 수 있게 하는 커스텀 쿼리
    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(FreeBoardSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class HirePostStaffSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    tag_set = serializers.SerializerMethodField()

    def get_tag_set(self, obj):
        return obj.extract_tag_list()

    class Meta:
        model = HirePostStaff
        fields = ('id', 'hit', 'author_username', 'thumbs', 'created_at',
                  'updated_at', 'title', 'context', 'image', 'category',
                  'tag_set', 'like_user_set', 'payment', 'requirement', 'advantage',
                  'job_loca', 'company', 'company_loca', 'company_desc', 'deadline',
                  'company_url', 'job_position'
                  )
        read_only_fields = read_only_fields_global


class HirePostActorSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    tag_set = serializers.SerializerMethodField()

    def get_tag_set(self, obj):
        return obj.extract_tag_list()

    class Meta:
        model = HirePostActor
        fields = ('id', 'hit', 'author_username', 'thumbs', 'created_at',
                  'updated_at', 'title', 'context', 'image', 'category',
                  'tag_set', 'like_user_set', 'payment', 'requirement', 'advantage',
                  'job_loca', 'company', 'company_loca', 'company_desc', 'deadline',
                  'company_url', 'job_position'
                  )
        read_only_fields = read_only_fields_global


class ResumeStaffSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = ResumeStaff
        fields = '__all__'
        read_only_fields = read_only_fields_global

class ResumeActorSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = ResumeActor
        fields = '__all__'
        read_only_fields = read_only_fields_global


class QnASerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = QnA
        fields = '__all__'
        read_only_fields = read_only_fields_global

