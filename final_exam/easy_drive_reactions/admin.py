from django.contrib import admin
from final_exam.easy_drive_reactions.models import Like, Comment

# Register your models here.


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('blog', 'owner', 'id')
    list_filter = ('blog', 'owner', 'id')
    ordering = ("-id", )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('ad', 'id', 'owner', 'published', 'content')
    list_filter = ('ad', 'id', 'owner', 'published', 'content')
    ordering = ("-published",)
