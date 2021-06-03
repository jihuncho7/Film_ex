from django.db import models
from django.conf import settings

# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# class FilmList(BaseModel):  # review_list,  의 데이터
#     #author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='my_post_set', on_delete=models.CASCADE)
#     title = models.CharField(max_length=20)
#     url = models.URLField(blank=True)
#     photo = models.ImageField(upload_to="film/film/%Y/%m/%d",blank=True)
#     context = models.TextField()
#     # director = models.CharField(max_length=10)
#     # genre_set = models.ManyToManyField('Genre', blank=True)
#     # tag_set = models.ManyToManyField('Tag', blank=True)
#     # like_user_set = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,
#     #                                        related_name='like_post_set')

