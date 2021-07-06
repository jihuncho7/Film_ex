

from .models import *
from rest_framework import serializers
from .serializer_comments import *

read_only_fields_global = (['author'])



class FilmSerializer(serializers.ModelSerializer):

    rate_show = serializers.SerializerMethodField()
    author_username = serializers.ReadOnlyField(source='author.username')
    postfrom = serializers.SerializerMethodField()

    def get_postfrom(self,obj):
        return '영화리뷰'

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


class FreeBoardSerializer(serializers.ModelSerializer, object):
    # user = serializers.ReadOnlyField(source='user.nickname')
    get_likes = serializers.SerializerMethodField()

    tag_set = serializers.SerializerMethodField()
    author_username = serializers.ReadOnlyField(source='author.username')
    is_like_user = serializers.SerializerMethodField()
    CommentFreeBoard = CommentFreeBoardSerializer(many=True,read_only=True)
    postfrom = serializers.SerializerMethodField()
    def get_postfrom(self,obj):
        return '자유게시판'
    def get_get_likes(self, obj):
        return obj.get_likes()


    def get_tag_set(self, obj):
        return obj.extract_tag_list()

    def get_is_like_user(self, instance):
        return instance.is_like_user(self.context['request'].user)

    class Meta:
        model = FreeBoard
        fields = ('id','hit','author_username','get_likes','created_at',
                  'updated_at','title','context','image','category',
                  'tag_set','is_like_user','like_user_set','CommentFreeBoard','postfrom',
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

class FreeBoard_SubSerializer(serializers.ModelSerializer, object):
    postfrom = serializers.SerializerMethodField()
    author_username = serializers.ReadOnlyField(source='author.username')
    def get_postfrom(self,obj):
        return '자유게시판'
    class Meta:
        model = FreeBoard
        fields = ('id','hit','created_at','author_username',
                  'updated_at','title','context','image','category',
                  'tag_set','postfrom',
                  )
        read_only_fields = read_only_fields_global


class HirePostStaffSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    tag_set = serializers.SerializerMethodField()
    postfrom = serializers.SerializerMethodField()
    is_like_user = serializers.SerializerMethodField()
    is_applied_user = serializers.SerializerMethodField()

    def get_is_applied_user(self, instance):
        return instance.is_applied_user(self.context['request'].user)
    def get_is_like_user(self, instance):
        return instance.is_like_user(self.context['request'].user)

    def get_postfrom(self, obj):
        return '스탭 구인'

    def get_tag_set(self, obj):
        return obj.extract_tag_list()

    class Meta:
        model = HirePostStaff
        fields = ('id', 'hit', 'author_username', 'thumbs', 'created_at',
                  'updated_at', 'title', 'context', 'image', 'category',
                  'tag_set', 'like_user_set', 'payment', 'requirement', 'advantage',
                  'job_loca', 'company', 'company_loca', 'company_desc', 'deadline',
                  'company_url', 'job_position','postfrom','is_like_user','is_applied_user',
                  )
        read_only_fields = read_only_fields_global

    # views.py 에서 필드 수정 할 수 있게 하는 커스텀 쿼리
    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(HirePostStaffSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class HirePostActorSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    tag_set = serializers.SerializerMethodField()
    postfrom = serializers.SerializerMethodField()
    is_like_user = serializers.SerializerMethodField()

    def get_is_like_user(self, instance):
        return instance.is_like_user(self.context['request'].user)

    def get_postfrom(self, obj):
        return '액터 구인'

    def get_tag_set(self, obj):
        return obj.extract_tag_list()

    class Meta:
        model = HirePostActor
        fields = ('id', 'hit', 'author_username', 'thumbs', 'created_at',
                  'updated_at', 'title', 'context', 'image', 'category',
                  'tag_set', 'like_user_set', 'payment', 'requirement', 'advantage',
                  'job_loca', 'company', 'company_loca', 'company_desc', 'deadline',
                  'company_url', 'job_position','postfrom','is_like_user',
                  )
        read_only_fields = read_only_fields_global

    # views.py 에서 필드 수정 할 수 있게 하는 커스텀 쿼리
    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(HirePostActorSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class ResumeStaffSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    postfrom = serializers.SerializerMethodField()

    def get_postfrom(self, obj):
        return '스탭 이력서'

    class Meta:
        model = ResumeStaff
        fields = '__all__'
        read_only_fields = read_only_fields_global

class ResumeActorSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    postfrom = serializers.SerializerMethodField()

    def get_postfrom(self, obj):
        return '액터 이력서'

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

class MyHirePostStaffSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    tag_set = serializers.SerializerMethodField()
    postfrom = serializers.SerializerMethodField()

    def get_postfrom(self, obj):
        return '스탭 구인'

    def get_tag_set(self, obj):
        return obj.extract_tag_list()

    class Meta:
        model = HirePostStaff
        fields = ('id', 'hit', 'author_username', 'thumbs', 'created_at',
                  'updated_at', 'title', 'context', 'image', 'category',
                  'tag_set', 'like_user_set', 'payment', 'requirement', 'advantage',
                  'job_loca', 'company', 'company_loca', 'company_desc', 'deadline',
                  'company_url', 'job_position','postfrom',
                  )
        read_only_fields = read_only_fields_global


class MyHirePostActorSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    tag_set = serializers.SerializerMethodField()
    postfrom = serializers.SerializerMethodField()

    def get_postfrom(self, obj):
        return '액터 구인'

    def get_tag_set(self, obj):
        return obj.extract_tag_list()

    class Meta:
        model = HirePostActor
        fields = ('id', 'hit', 'author_username', 'thumbs', 'created_at',
                  'updated_at', 'title', 'context', 'image', 'category',
                  'tag_set', 'like_user_set', 'payment', 'requirement', 'advantage',
                  'job_loca', 'company', 'company_loca', 'company_desc', 'deadline',
                  'company_url', 'job_position','postfrom',
                  )
        read_only_fields = read_only_fields_global
