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
    context={
        'car': car,
        'insurance': insurance,
        'total_charges': total_charges,
    }

    return render(request, 'cars/car_detail.html', context=context)