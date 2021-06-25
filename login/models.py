from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from .managers import *

class User(AbstractBaseUser,PermissionsMixin):
    objects = CustomUserManager()
    image = models.ImageField(upload_to="login/%Y/%m/%d", blank=True)
    phone_regex = RegexValidator(regex=r'\d{9,15}$',
                                 message="Phone number must be entered in the format: '999999999'. Up to 15 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    email = models.EmailField(
        max_length=255,
        unique=True,
    )
    username = models.CharField(
        max_length=20,
        null=False,
        unique=True
    )
    social = models.CharField(max_length=10,null=True)
    # first_name = None
    # last_name = None
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']


    # realname = models.CharField('이름', blank=True, max_length=50)
    # nickname = models.CharField('닉네임', blank=True, max_length=50, null=True)
    # address = models.CharField('주소', blank=True, max_length=200, null=True)
    # phone = models.CharField('전화번호', blank=True, max_length=100, null=True)
    # date_of_birth = models.DateField('생년월일', blank=True, null=True)
    # profile_image = models.ImageField('프로필사진', blank=True, null=True)
    #
    # social = models.CharField('소셜', max_length=20, blank=True)