from django.db import models
from final_exam.easy_drive_profile.models import Profile


# Create your models here.

class BlogPost(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=30, blank=False, null=False)
    topic = models.CharField(max_length=50, blank=False, null=False)
    content = models.TextField(max_length=200, blank=False, null=False)
    published = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"title: {self.title} - blog_id: {self.id}"
