from django.contrib import admin
from final_exam.easy_drive_blog.models import BlogPost

# Register your models here.


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'owner', 'published')
    list_filter = ('title', 'id', 'owner', 'published')
    search_fields = ('title', )
    ordering = ('-published',)
