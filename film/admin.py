from django.contrib import admin
from .models import Film, Tag

# Register your models here.

@admin.register(Film)
class PostAdmin(admin.ModelAdmin):
    pass

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass