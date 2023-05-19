from uuid import uuid4
from colorfield.fields import ColorField
from members.models import CustomUser
from cars.models import Car
from cars.models import Reservation
from django.db import models

# Create your models here.
class PostIt(models.Model):
    id = models.UUIDField(primary_key=True, default = uuid4, editable=False)
    car = models.ForeignKey(Car, related_name="post_it", blank=False, null=False, on_delete=models.CASCADE)
    sender = models.ForeignKey(CustomUser, blank=False, null=False, on_delete=models.CASCADE)
    message = models.TextField(blank=False, max_length=500)
    color = ColorField(default='#219ebc')
    sent_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reservation = models.ForeignKey(Reservation, blank = True, null=True, related_name="reservation", on_delete=models.CASCADE)
    


    def __str__(self):
        return(self.car.name + ' - ' + self.sender.username + ' - ' + str(self.sent_at))
    
class PostItNotShowed(models.Model):
    user = models.ForeignKey(CustomUser, related_name="showed", on_delete=models.CASCADE)
    post_it = models.ForeignKey(PostIt, related_name="showed", on_delete=models.CASCADE)