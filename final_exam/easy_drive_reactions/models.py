from django.db import models
from final_exam.easy_drive_profile.models import Profile
from final_exam.easy_drive_ad.models import Ad
from final_exam.easy_drive_blog.models import BlogPost


# Create your models here.

class Like(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE)

    def __str__(self):
        return f"owner: {self.owner} - blog: {self.blog} - like_id: {self.id}"


class Comment(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    content = models.TextField(max_length=100, blank=False, null=False)
    published = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"owner: {self.owner} - ad: {self.ad} - comment_id: {self.id}"
