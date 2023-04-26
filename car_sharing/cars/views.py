from django.shortcuts import render
from .models import *
from members.models import CustomUser

# Create your views here.
def car_detail_view(request, id, slug):
    car = Car.objects.get(id=id)
    users = car.users.all()
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
        trips_car = Trip.objects.filter(car=car)
        for i in trips_car:
            nb_km = i.nb_km_end - i.nb_km_start
            nb_km_total += nb_km

    trips_by_user = []
    for user in users:
        if Trip.objects.filter(car = car, user=user).exists():
            user_trips = Trip.objects.filter(car=car, user=user)
            nb_km_total_user = 0
            for trip in user_trips:
                nb_km_trip = trip.nb_km_end - trip.nb_km_start
                nb_km_total_user += nb_km_trip
            trips = ({'user': user, 'nb_km_trip': nb_km_total_user})
            trips_by_user.append(trips)



    context={
        'car': car,
        'insurance': insurance,
        'insurance_price': insurance_price,
        'total_charges': total_charges,
        'car_paid_by': car_paid_by,
        'nb_km_total': nb_km_total,
        'trips_by_user': trips_by_user
    }

    return render(request, 'cars/car_detail.html', context=context)