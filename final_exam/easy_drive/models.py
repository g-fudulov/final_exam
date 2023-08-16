from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class MyUser(AbstractUser):
    username = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.username}"
