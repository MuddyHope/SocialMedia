from email.policy import default
from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  #extend the user model
    id_user = models.IntegerField()
    bio = models.TextField(max_length = 100, blank = True)
    profileimg = models.ImageField(upload_to = 'profile_images', default = 'default-pic.JPG')            #place to store the image in profile_images
    location = models.CharField(max_length = 100, blank = True)
    
    def __str__(self):
        return self.user.username