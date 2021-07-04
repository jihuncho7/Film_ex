# from drf_haystack.serializers import HaystackSerializer
# from haystack import indexes
# from rest_framework import serializers
#
# from .models import Film, FreeBoard, HirePostStaff, HirePostActor
# from .serializer import FilmSerializer,FreeBoardSerializer,HirePostStaffSerializer,HirePostActorSerializer
#
#
#
# class FilmIndex(indexes.SearchIndex, indexes.Indexable):
#     text = indexes.CharField(document=True, use_template=True)
#
#
#     def get_model(self):
#         return Film
#
# class FreeBoardIndex(indexes.SearchIndex, indexes.Indexable):
#     text = indexes.CharField(document=True, use_template=True)
#
#     def get_model(self):
#         return FreeBoard
#
# class HirePostStaffIndex(indexes.SearchIndex, indexes.Indexable):
#     text = indexes.CharField(document=True, use_template=True)
#
#     def get_model(self):
#         return HirePostStaff
#
# class HirePostActorIndex(indexes.SearchIndex, indexes.Indexable):
#     text = indexes.CharField(document=True, use_template=True)
#
#     def get_model(self):
#         return HirePostActor
#
# class AggregateSearchSerializer(HaystackSerializer):
#     class Meta:
#         serializers = {
#             FilmIndex: FilmSerializer,
#             FreeBoardIndex: FreeBoardSerializer,
#             HirePostStaffIndex: HirePostStaffSerializer,
#             HirePostActorIndex: HirePostActorSerializer,
#
#         }