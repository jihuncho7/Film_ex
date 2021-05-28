from django.contrib import admin
from django.contrib.auth.models import User
from .models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = (
        'email',
        'date_joined',
        'username',
    )

    list_display_links = (
        'email',
        'username',
    )