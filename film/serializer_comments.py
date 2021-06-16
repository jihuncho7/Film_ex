"""

코멘트 시리얼라이저

"""
from .models import *
from rest_framework import serializers

read_only_fields_global = (['author'])

"""

영화 리뷰 코멘트

"""


class CommentInCommentSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = CommentInComment
        fields = '__all__'
        read_only_fields = read_only_fields_global


class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    CommentInComment = CommentInCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = read_only_fields_global

"""

자유게시판 코멘트

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


"""

스태프 구인 코멘트

"""
class CommentInCommentHirePostStaffSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = CommentInCommentHirePostStaff
        fields = '__all__'
        read_only_fields = read_only_fields_global

class CommentHirePostStaffSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    CommentInCommentHirePostStaff = CommentInCommentHirePostStaffSerializer(many=True,read_only=True)
    class Meta:
        model = CommentHirePostStaff
        fields = '__all__'
        read_only_fields = read_only_fields_global


"""

구인 액터 코멘트

"""

class CommentInCommentHirePostActorSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = CommentInCommentHirePostStaff
        fields = '__all__'
        read_only_fields = read_only_fields_global

class CommentHirePostActorSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    CommentInCommentHirePostActor = CommentInCommentHirePostActorSerializer(many=True,read_only=True)
    class Meta:
        model = CommentHirePostActor
        fields = '__all__'
        read_only_fields = read_only_fields_global

