from django.contrib import admin
from final_exam.easy_drive_ad.models import Ad
# Register your models here.


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ("title", 'id', "owner", 'price', "published")
    list_filter = ("title", 'id', "owner", 'price', "published")
    search_fields = ('title', )
    ordering = ('-published',)
