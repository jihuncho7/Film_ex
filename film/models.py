import re
from django.conf import settings
from django.db import models
from django.urls import reverse


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Film(BaseModel):  # review_list,  의 데이터
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='my_post_set', on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    url = models.URLField(blank=True)
    photo = models.ImageField(upload_to="film/film/%Y/%m/%d",blank=True)
    context = models.TextField()
    director = models.CharField(max_length=10)
    genre_set = models.ManyToManyField('Genre', blank=True)
    tag_set = models.ManyToManyField('Tag', blank=True)
    like_user_set = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,
                                           related_name='like_post_set')




    def __str__(self):
        return self.title

    def is_like_user(self, user):
        return self.like_user_set.filter(pk=user.pk).exists()

    def extract_tag_list(self):
        tag_name_list = re.findall(r"#([a-zA-Z\dㄱ-힣]+)", self.context)
        tag_list = []
        for tag_name in tag_name_list:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            tag_list.append(tag)
        return tag_list

    def get_absolute_url(self):
        return reverse("film:review_detail", args=[self.pk])

    class Meta:
        ordering = ['-created_at']


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Comment(BaseModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Film, on_delete=models.CASCADE)
    message = models.TextField()

    class Meta:
        ordering = ['-id']

# class Hire_Board(BaseModel): # 구인 공고
#     title = models.CharField(max_length=20)
#     pic = models.ImageField(null=True)
#     requirement = models.TextField()
#     prefer = models.TextField(null=True)
#     location = models.CharField(max_length=30)
#     fee = models.IntegerField()
#     rating = models.TextField(null=True)
#
# class Qna(models.Model):
#     qna_author = models.CharField(max_length=10)
#     qna_email = models.EmailField()
#     qna_title = models.CharField(max_length=30)
#     qna_context = models.TextField()
#     qna_file = models.FileField(null=True)
#     qna_dt = models.DateField(auto_now=True)
#
# class Review(models.Model):
#     rw_title = models.CharField(max_length=20)
#     rw_author = models.CharField(max_length=10)
#     rw_context = models.TextField()
#     rw_dt_write = models.DateField(auto_now=True)
#     rw_rating = models.FloatField()








