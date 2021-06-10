from django.contrib import admin
from .models import Film, Genre, Comment, FreeBoard, ResumeStaff


# Register your models here.

@admin.register(Film)
class PostAdmin(admin.ModelAdmin):
    pass
@admin.register(Genre)
class TagAdmin(admin.ModelAdmin):
    pass
@admin.register(Comment)
class TagAdmin(admin.ModelAdmin):
    pass

@admin.register(FreeBoard)
class FreeBoardAdmin(admin.ModelAdmin):
    pass
@admin.register(ResumeStaff)
class ResumeStaffAdmin(admin.ModelAdmin):
    pass