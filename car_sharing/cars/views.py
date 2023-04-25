from django.shortcuts import render
from .models import *

# Create your views here.
def car_detail_view(request, id, slug):
    car = Car.objects.get(id=id)
    
    insurance_price = 0
    insurance = ""
    if Insurance.objects.filter(car=car).exists():
        insurance = Insurance.objects.get(car=car)
        insurance_price = insurance.price

    total_charges = car.price + insurance_price

    car_paid_by=None
    if PurchaseParticipation.objects.filter(car=car).exists():
        car_paid_by = PurchaseParticipation.objects.filter(car=car)

    nb_km_total = 0

    if Trip.objects.filter(car = car).exists():
        trips = Trip.objects.filter(car=car)
        for i in trips:
            nb_km = i.nb_km_end - i.nb_km_start
            nb_km_total += nb_km

    context={
        'car': car,
        'insurance': insurance,
        'insurance_price': insurance_price,
        'total_charges': total_charges,
        'car_paid_by': car_paid_by,
        'nb_km_total': nb_km_total,
    }

    return render(request, 'cars/car_detail.html', context=context)