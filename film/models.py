from django.db import models

# Create your models here.
class Film(models.Model):  # review_list,  의 데이터
    title = models.CharField(max_length=20)
    dates = models.DateField(auto_now=True)
    thumb = models.IntegerField()
    url = models.URLField()
    context = models.TextField()
    director = models.CharField(max_length=10)
    genre = models.CharField(max_length=10)

class User_I(models.Model): # 개인
    email = models.EmailField()
    name = models.CharField(max_length=8)

class User_C(models.Model): # 기업
    email = models.EmailField()
    name = models.CharField(max_length=20)

class Hire_Board(models.Model): # 구인 공고
    title = models.CharField(max_length=20)
    dt_write = models.DateField(auto_now_add=True)
    dt_mod = models.DateField(auto_now_add=True)
    pic = models.ImageField(null=True)
    requirement = models.TextField()
    prefer = models.TextField(null=True)
    location = models.CharField(max_length=30)
    fee = models.IntegerField()
    rating = models.TextField(null=True)
    tag =

class Qna(models.Model):
    qna_author = models.CharField(max_length=10)
    qna_email = models.EmailField()
    qna_title = models.CharField(max_length=30)
    qna_context = models.TextField()
    qna_file = models.FileField(null=True)
    qna_dt = models.DateField(auto_now=True)
    qna_tag
class Review(models.Model):
    rw_title = models.CharField(max_length=20)
    rw_author = models.CharField(max_length=10)
    rw_context = models.TextField()
    rw_dt_write = models.DateField(auto_now=True)
    rw_rating = models.FloatField()
    rw_tag







