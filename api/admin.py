from django.contrib import admin
from .models import FilmList


# Register your models here.

@admin.register(FilmList)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'photo']
    pass
