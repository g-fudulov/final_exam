from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class MyUser(AbstractUser):
    username = models.CharField(max_length=20, unique=True)


class Profile(models.Model):
    user = models.OneToOneField('MyUser', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    phone_number = models.CharField(max_length=13, blank=True, null=True)
    created_on = models.DateField(auto_now=True)


class Ad(models.Model):
    owner = models.ForeignKey('Profile', on_delete=models.CASCADE)
    cover_photo = models.URLField(max_length=205, blank=False, null=False)
    additional_photo = models.URLField(max_length=205, blank=False, null=False)
    title = models.CharField(max_length=30, blank=False, null=False)
    description = models.TextField(max_length=200)
    published = models.DateTimeField(auto_now_add=True)
    price = models.PositiveIntegerField(blank=False, null=False)


class BlogPost(models.Model):
    owner = models.ForeignKey('Profile', on_delete=models.CASCADE)
    title = models.CharField(max_length=30, blank=False, null=False)
    topic = models.CharField(max_length=50, blank=False, null=False)
    content = models.TextField(max_length=200, blank=False, null=False)
    published = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    owner = models.ForeignKey('Profile', on_delete=models.CASCADE)
    blog = models.ForeignKey('BlogPost', on_delete=models.CASCADE)


class Comment(models.Model):
    owner = models.ForeignKey('Profile', on_delete=models.CASCADE)
    ad = models.ForeignKey('Ad', on_delete=models.CASCADE)
    content = models.TextField(max_length=100, blank=False, null=False)
    published = models.DateTimeField(auto_now_add=True)
