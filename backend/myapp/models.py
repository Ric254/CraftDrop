from django.contrib.auth.models import AbstractUser
from django.db import models
import os

def profile_picture_path(instance, filename):
    #Generate upload path for profile pictures
    return os.path.join('profile_pictures', f'user_{instance.user_id}', filename)

def artwork_file_path(instance, filename):
    #Generate upload path for artworks
    return os.path.join('artworks', f'artwork_{instance.user_id}', filename)


class User(AbstractUser):
    user_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length = 45)
    last_name = models.CharField(max_length = 45)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(max_length=200, null=True, blank=True)
    profile_picture = models.ImageField(upload_to=profile_picture_path, null=True)

class Artists(models.Model):
    artist_id = models.IntegerField(primary_key=True)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, related_name='artist')
    location = models.CharField(max_length=45)
    style = models.CharField(max_length=45)


    @property
    def bio(self):
        return self.user_id.bio
    def save(self, *args, **kwargs):
        if self.user_id and self.user_id.bio:
            self.user_id.bio = self.bio
            self.user_id.save()
        super().save(*args, **kwargs)

class Address(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, related_name='address')
    street = models.CharField(max_length= 45)
    city = models.CharField(max_length = 45)
    state = models.CharField(max_length = 45)
    country = models.CharField(max_length = 45)
    zipcode = models.CharField(max_length = 45)

class Artwork(models.Model):
    artwork_id = models.IntegerField(primary_key=True)
    artist_id = models.ForeignKey(Artists, on_delete=models.CASCADE, related_name='artworks')
    title = models.CharField(max_length = 45)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=8,  decimal_places=2)
    medium = models.CharField(max_length = 45)
    height = models.DecimalField(max_digits=8, decimal_places=2)
    width = models.DecimalField(max_digits = 8, decimal_places=2)
    depth = models.DecimalField(max_digits=8, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to=artwork_file_path)

    def is_picture(self):
        #Checks if file is a picture
        return self.filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))
    

    def is_video(self):
        #Checks if file is a video
        return self.filename.lower().endswith(('.mp4', '.avi', '.mov'))

class Order(models.Model):
    order_id = models.IntegerField(primary_key=True)
    artwork_id = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    date_ordered = models.DateTimeField(auto_now_add=True)
    status = None
