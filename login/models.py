from django.conf import settings
from django.db import models

# Create your models here.



class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # 현 계정의 사용자를 가져올 수 있음.
    nickname = models.CharField(max_length=64)
    profile_photo = models.ImageField(upload_to="login/profile/%Y/%m",blank=True)
