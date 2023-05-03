from django.contrib import admin
from .models import *

# Register your models here.
class CarAdmin(admin.ModelAdmin):
    list_display= ('name', 'creation_at', 'updated_at')


class PurchaseParticipationAdmin(admin.ModelAdmin):
    list_display = ('car', 'user', 'price_paid')

class InsuranceAdmin(admin.ModelAdmin):
    list_display = ('car', 'price', 'company', 'renewal_date')

class InsuranceParticipationAdmin(admin.ModelAdmin):
    list_display = ('insurance', 'user', 'price_paid')

class TripAdmin(admin.ModelAdmin):
    readonly_fields = ('nb_km',)
    def nb_km(self, obj):
        return obj.nb_km_end - obj.nb_km_start

    list_display = ('car', 'user', 'nb_km', 'start', 'end')

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('car', 'user', 'reservation_start', 'reservation_end')

class EnergyAdmin(admin.ModelAdmin):
    list_display = ('car', 'price', 'paid_by', 'paid_day')

class RepairAdmin(admin.ModelAdmin):
    list_display = ('car', 'price', 'paid_by', 'paid_day', 'type_repair')


admin.site.register(Car, CarAdmin)
admin.site.register(PurchaseParticipation, PurchaseParticipationAdmin)
admin.site.register(Insurance, InsuranceAdmin)
admin.site.register(InsuranceParticipation, InsuranceParticipationAdmin)
admin.site.register(Trip, TripAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Energy, EnergyAdmin)
admin.site.register(Repair, RepairAdmin)