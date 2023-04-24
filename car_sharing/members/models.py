import os
from uuid import uuid4
from django.contrib.auth.models import AbstractUser
from PIL import Image
from django.db import models

#function to rename avatar file on upload
def path_and_rename(instance, filename):
    upload_to = 'members_avatars'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)

class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default = uuid4, editable=False)
    email = models.EmailField(unique=True)
    creation_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    avatar = models.ImageField(upload_to=path_and_rename, max_length=255, null=True, blank=True)
    is_rgpd = models.BooleanField(default=False)

    # resizing images
    def save(self, *args, **kwargs):
        super().save()
        if self.avatar:
            img = Image.open(self.avatar.path)

            if img.height > 100 or img.width > 100:
                new_img = (100, 100)
                img.thumbnail(new_img)
                img.save(self.avatar.path)
        else:
            pass


    def __str__(self):
        return self.email
    

