from django.contrib import admin
from .models import *

# Register your models here.
class CarAdmin(admin.ModelAdmin):
    list_display= ('name', 'creation_at', 'updated_at')


class PurchaseParticipationAdmin(admin.ModelAdmin):
    list_display = ('car', 'user', 'price_paid')

class InsuranceAdmin(admin.ModelAdmin):
    list_display = ('car', 'price', 'paid_by', 'company', 'renewal_date')

class TripAdmin(admin.ModelAdmin):
    readonly_fields = ('nb_km',)
    def nb_km(self, obj):
        return obj.nb_km_end - obj.nb_km_start

    list_display = ('car', 'user', 'nb_km', 'start', 'end')


admin.site.register(Car, CarAdmin)
admin.site.register(PurchaseParticipation, PurchaseParticipationAdmin)
admin.site.register(Insurance, InsuranceAdmin)
admin.site.register(Trip, TripAdmin)