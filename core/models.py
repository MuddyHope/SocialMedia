from email.policy import default
from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.
import uuid  #used for random generation
from datetime import datetime


User = get_user_model()


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  #extend the user model
    id_user = models.IntegerField()
    bio = models.TextField(max_length = 100, blank = True)
    profileimg = models.ImageField(upload_to = 'profile_images', default = 'default-pic.JPG')            #place to store the image in profile_images
    location = models.CharField(max_length = 100, blank = True)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    id = models.UUIDField(primary_key = True, default= uuid.uuid4)
    username = models.CharField(max_length = 100)  #
    image = models.ImageField(upload_to = 'post_images')
    caption = models.TextField(max_length = 50)
    created_at = models.DateTimeField(default= datetime.now)
    no_of_likes = models.IntegerField(default = 0)

    def __str__(self):
        return self.username


class LikePost(models.Model):
    post_id = models.CharField(max_length = 100)
    username = models.CharField(max_length = 100)

    def __str__(self) -> str:
        return self.username

class FollowerCount(models.Model):
    follower = models.CharField(max_length = 100)
    username = models.CharField(max_length = 100)

    def __str__(self) -> str:
        return self.username