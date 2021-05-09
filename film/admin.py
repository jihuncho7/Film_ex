from django.contrib import admin
from .models import Film,  Genre, Comment


# Register your models here.

@admin.register(Film)
class PostAdmin(admin.ModelAdmin):
    pass
@admin.register(Genre)
class TagAdmin(admin.ModelAdmin):
    pass
@admin.register(Comment)
class TagAdmin(admin.ModelAdmin):
    list_display = [ 'post', 'author' ]
    pass