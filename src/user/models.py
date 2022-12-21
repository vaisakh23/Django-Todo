from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import os 


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default= 'image/default.png', upload_to='image', blank=True)
    
    def save(self, *args, **kwargs):
        # override the save method to resize images
        profile = super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 200 and img.width > 200:
            new_size = (200, 200)
            img.thumbnail(new_size)
            img.save(self.image.path)
        return profile
    
    @staticmethod
    def remove_old_img(request, path):
        if request.user.profile.image.path != path and os.path.basename(path) != 'default.png':
            os.remove(path)
