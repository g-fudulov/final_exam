from django.contrib import admin
from ..easy_drive import models as my_models


# Register your models here.
@admin.register(my_models.MyUser)
class MyUserAdmin(admin.ModelAdmin):
    list_filter = ('username', "id")
    list_display = ('username', "id")
    search_fields = ('username', "id")
    ordering = ('-id', )
