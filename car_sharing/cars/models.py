from django.utils.translation import gettext as _
import os
from uuid import uuid4
from django.utils.text import slugify
from PIL import Image
from members.models import CustomUser
from django.db import models

#function to rename avatar file on upload
def path_and_rename(instance, filename):
    upload_to = 'cars_pictures'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)

# Create your models here.
class Car(models.Model):
    ESSENCE= _('essence')
    DIESEL = _('diesel')
    ÉLECTRICITÉ = _('électricité')
    HYBRIDE_NO = _('hybride non rechargeable')
    HYBRIDE= _('hybride rechargeable')
    GPL = _('gpl')
    ENERGY = [
        (ESSENCE, _("Fonctionne à l'essence")),
        (DIESEL, _("Fonctionne au diesel")),
        (ÉLECTRICITÉ, _("Véhicule électrique")),
        (HYBRIDE_NO, _("Véhicule hybride non rechargeable")),
        (HYBRIDE, _("Véhicule hybride rechargeable")),
        (GPL, _("Fonctionne au GPL")),
    ]
    id = models.UUIDField(primary_key=True, default = uuid4, editable=False)
    name = models.CharField(max_length=255, null=False, blank = False)
    users = models.ManyToManyField(CustomUser, blank=False, related_name="car_users")
    immatriculation = models.CharField(max_length=100, blank = True, null = True)
    energy = models.CharField(max_length=32, choices = ENERGY, default=ESSENCE)
    picture = models.ImageField(upload_to=path_and_rename, max_length=255, null=True, blank = True)
    price = models.FloatField(max_length=100, null=True, blank = True)
    slug = models.SlugField(max_length=255, unique= True, default=None, null=True)
                             
    creation_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # resizing images
    def save(self, *args, **kwargs):
        super().save()
        if self.picture:
            img = Image.open(self.picture.path)

            if img.height > 200 or img.width > 200:
                new_img = (200, 200)
                img.thumbnail(new_img)
                img.save(self.picture.path)
        else:
            pass
        if not self.slug:
            self.slug = slugify(self.name)
        super(Car, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class PurchaseParticipation(models.Model):
    car = models.ForeignKey(Car, related_name="purchase_participation", blank=False, null=False, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, related_name="user_participation", blank=False, null=False, on_delete=models.PROTECT)
    price_paid = models.FloatField(max_length=100, null=False, blank=False)

class Insurance(models.Model):
    car = models.ForeignKey(Car, related_name="insurance", blank=False, null=False, on_delete=models.CASCADE)
    company = models.CharField(max_length=255, blank=False, null=False)
    price = models.FloatField(max_length=100, null=False, blank=False)
    paid_by = models.ForeignKey(CustomUser, null=False, blank=False, on_delete=models.PROTECT)
    renewal_date = models.DateField(auto_now_add=False, null=True, blank=True)

class Trip(models.Model):
    car = models.ForeignKey(Car, related_name="trip", null=False, blank=False, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, null=False, blank=False, related_name="user_trip", on_delete=models.PROTECT)
    nb_km_start = models.IntegerField(null=False, blank=False, default=0)
    nb_km_end = models.IntegerField(null=False, blank=False, default=0)
    start = models.DateField(null=False, blank=False, auto_now_add=False)
    end = models.DateField(null=False, blank=False, auto_now_add=False)