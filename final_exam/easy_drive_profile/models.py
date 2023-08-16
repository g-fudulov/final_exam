from django.db import models
from final_exam.easy_drive.models import MyUser


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    phone_number = models.CharField(max_length=13, blank=True, null=True)
    created_on = models.DateField(auto_now=True)

    def __str__(self):
        return f"username: {self.user} - id: {self.id}"
