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
    if instance.slug:
        filename = '{}.{}'.format(instance.slug, ext)
    elif instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)

def path_and_rename_bill(instance, filename):
    upload_to = 'bills_pictures'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.car, ext)
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
    nb_users = models.IntegerField(null=False, blank = False, default=2)
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
            self.slug = slugify(self.name + '_' + str(self.id))
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
    renewal_date = models.DateField(auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return self.car.name + '_' + str(self.renewal_date)

class InsuranceParticipation(models.Model):
    insurance = models.ForeignKey(Insurance, related_name="insurance_participation", null=False, blank=False, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, related_name="user_insurance_participation", blank=False, null=False, on_delete=models.PROTECT)
    price_paid = models.FloatField(max_length=100, null=False, blank=False)

    

class Trip(models.Model):
    car = models.ForeignKey(Car, related_name="trip", null=False, blank=False, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, null=False, blank=False, related_name="user_trip", on_delete=models.PROTECT)
    nb_km_start = models.IntegerField(null=False, blank=False, default=0)
    nb_km_end = models.IntegerField(null=False, blank=False, default=0)
    start = models.DateField(null=False, blank=False, auto_now_add=False)
    end = models.DateField(null=False, blank=False, auto_now_add=False)

class Reservation(models.Model):
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    REJECTED = 'rejected'
    CANCELLED = 'cancelled'
    ON_GOING = 'on_going'
    RETURNED = 'returned'
    STATUS = [
        (PENDING, ('Waiting for confirmation')),
        (CONFIRMED, ('Confirmed')),
        (REJECTED, ('Cancelled by owner')),
        (CANCELLED, ('Cancelled by requester')),
        (ON_GOING, ('Product actually borrowed by requester ')),
        (RETURNED, ('Product returned by the borrower')),
    ]
    id = models.UUIDField(primary_key=True, default = uuid4, editable=False)
    car = models.ForeignKey(Car, related_name="reservation", null=False, blank=False, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, null=False, blank=False, related_name="user_reservation", on_delete=models.PROTECT)
    demand_date = models.DateField(auto_now_add=True)
    reservation_start = models.DateTimeField(null=False, blank=False, auto_now_add=False)
    reservation_end = models.DateTimeField(null=False, blank=False, auto_now_add=False)
    status = models.CharField(max_length=32, choices = STATUS, default=PENDING)

    def __str__(self):
        return self.car.name + ' - ' + self.user.username + ' - ' + str(self.reservation_start)



class Energy(models.Model):
    ESSENCE= _('essence')
    DIESEL = _('diesel')
    ÉLECTRICITÉ = _('électricité')
    GPL = _('gpl')
    ENERGY = [
        (ESSENCE, _("essence")),
        (DIESEL, _("diesel")),
        (ÉLECTRICITÉ, _("kwatt")),
        (GPL, _("GPL")),
    ]
    car = models.ForeignKey(Car, related_name="energy_bill", null=False, blank=False, on_delete=models.CASCADE)
    price = models.FloatField(max_length=100, null=False, blank=False, default=0)
    quantity = models.FloatField(max_length=100, null=False, blank=False, default=0)
    paid_by = models.ForeignKey(CustomUser, null=False, blank=False, related_name="user_energy_bill", on_delete=models.PROTECT)
    paid_day = models.DateField(auto_now_add=False)
    type_energy = models.CharField(max_length=32, choices = ENERGY, default=ESSENCE)
    picture = models.ImageField(upload_to=path_and_rename_bill, max_length=255, null=True, blank = True)
    slug = models.SlugField(max_length=255, unique= True, default=None, null=True)

    def save(self, *args, **kwargs):
        super().save()
        if self.picture:
            img = Image.open(self.picture.path)

            if img.height > 600 or img.width > 200:
                new_img = (600, 200)
                img.thumbnail(new_img)
                img.save(self.picture.path)
        else:
            pass
        if not self.slug:
            self.slug = slugify(self.car + '_' + self.paid_day)
        super(Energy, self).save(*args, **kwargs)

class Repair(models.Model):
    ENTRETIEN= _('entretien')
    IMPORTANT = _('importante')
    
    TYPE = [
        (ENTRETIEN, _("entretien")),
        (IMPORTANT, _("réparation importante")),
        
    ]
    car = models.ForeignKey(Car, related_name="repair_bill", null=False, blank=False, on_delete=models.CASCADE)
    price = models.FloatField(max_length=100, null=False, blank=False, default=0)
    description = models.TextField(max_length=500, blank=True, null=True)
    paid_by = models.ForeignKey(CustomUser, null=False, blank=False, related_name="user_repair_bill", on_delete=models.PROTECT)
    paid_day = models.DateField(auto_now_add=False)
    type_repair = models.CharField(max_length=32, choices = TYPE, default=ENTRETIEN)
    picture = models.ImageField(upload_to=path_and_rename_bill, max_length=255, null=True, blank = True)
    slug = models.SlugField(max_length=255, unique= True, default=None, null=True)

    def save(self, *args, **kwargs):
        super().save()
        if self.picture:
            img = Image.open(self.picture.path)

            if img.height > 600 or img.width > 200:
                new_img = (600, 200)
                img.thumbnail(new_img)
                img.save(self.picture.path)
        else:
            pass
        if not self.slug:
            self.slug = slugify(self.car + '_' + self.paid_day)
        super(Repair, self).save(*args, **kwargs)