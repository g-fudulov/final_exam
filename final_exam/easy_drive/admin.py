from django.contrib import admin
from ..easy_drive import models as my_models


# Register your models here.
@admin.register(my_models.MyUser)
class MyUserAdmin(admin.ModelAdmin):
    list_filter = ('username', "id")
    list_display = ('username', "id")
    search_fields = ('username', "id")
    ordering = ('-id', )


@admin.register(my_models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "id", "first_name", "last_name", "phone_number", "created_on")
    list_filter = ("user", "id", "first_name", "last_name", "phone_number", "created_on")
    search_fields = ('first_name', "last_name", "phone_number")
    ordering = ("-created_on", )


@admin.register(my_models.Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ("title", 'id', "owner", 'price', "published")
    list_filter = ("title", 'id', "owner", 'price', "published")
    search_fields = ('title', )
    ordering = ('-published',)


@admin.register(my_models.BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'owner', 'published')
    list_filter = ('title', 'id', 'owner', 'published')
    search_fields = ('title', )
    ordering = ('-published',)


@admin.register(my_models.Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('blog', 'owner', 'id')
    list_filter = ('blog', 'owner', 'id')
    ordering = ("-id", )


@admin.register(my_models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('ad', 'id', 'owner', 'published', 'content')
    list_filter = ('ad', 'id', 'owner', 'published', 'content')
    ordering = ("-published",)
