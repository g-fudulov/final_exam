from django.contrib import admin
from final_exam.easy_drive_profile.models import Profile


# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "id", "first_name", "last_name", "phone_number", "created_on")
    list_filter = ("user", "id", "first_name", "last_name", "phone_number", "created_on")
    search_fields = ('first_name', "last_name", "phone_number")
    ordering = ("-created_on",)
