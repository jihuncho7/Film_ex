from django.contrib import admin
from .models import Film, Tag, Genre, Comment


# Register your models here.

@admin.register(Film)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'photo', 'created_at', 'updated_at']
    pass

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass

@admin.register(Genre)
class TagAdmin(admin.ModelAdmin):
    pass
@admin.register(Comment)
class TagAdmin(admin.ModelAdmin):
    list_display = [ 'post', 'author' ]
    pass