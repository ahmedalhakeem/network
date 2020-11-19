from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField('self', symmetrical=False, related_name="followers")
    picture = models.ImageField(height_field="hieght_field", width_field="widt_field", upload_to='media/', null=True, blank=True)
    height_field = models.IntegerField(default=0)
    width_fiels = models.IntegerField(default=0)

class Post(models.Model):
    content = models.TextField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="poster")
    like = models.ManyToManyField(User, related_name="user_like")
    image = models.ImageField(default = False ,upload_to ='media/')
    
    def __str__(self):
        return f"{self.content}, {self.timestamp},{self.created_by}, {self.image}"



#class Follow(models.Model):
 #   follower = models.ManyToManyField(User,  related_name="following+")
  #  following = models.ManyToManyField(User, related_name="followers+")

    



