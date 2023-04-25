from django.contrib import admin
from .models import *

# Register your models here.
class CarAdmin(admin.ModelAdmin):
    list_display= ('name', 'creation_at', 'updated_at')
admin.site.register(Car, CarAdmin)

class PurchaseParticipationAdmin(admin.ModelAdmin):
    list_display = ('car', 'user', 'price_paid')

admin.site.register(PurchaseParticipation, PurchaseParticipationAdmin)