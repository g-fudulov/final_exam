from django.db import models
from final_exam.easy_drive_profile.models import Profile
# Create your models here.


class Ad(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    cover_photo = models.URLField(max_length=205, blank=False, null=False)
    additional_photo = models.URLField(max_length=205, blank=False, null=False)
    title = models.CharField(max_length=30, blank=False, null=False)
    description = models.TextField(max_length=350)
    published = models.DateTimeField(auto_now_add=True)
    price = models.PositiveIntegerField(blank=False, null=False)

    def __str__(self):
        return f"title: {self.title} - ad_id: {self.id}"
