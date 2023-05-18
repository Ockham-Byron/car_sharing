from django.utils.translation import gettext as _
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import *
from cars.models import Car, Reservation

@login_required
def profile_view(request, id):
    user = CustomUser.objects.get(id=id)
    cars = Car.objects.filter(users__id__contains=user.id)
    car = None
    if len(cars) == 1:
        car = cars[0]

    reservations = None
    reservations_to_confirm = None
    for car in cars:
        if Reservation.objects.filter(car=car).exists():
            reservations = Reservation.objects.filter(car=car)
            reservations_to_confirm = reservations.filter(status = "pending").exclude(user=request.user)


    context = {
        'user': user,
        'car':car,
        'reservations': reservations,
        'reservations_to_confirm':reservations_to_confirm,
        }
    
    return render(request, 'members/profile.html', context=context)
@login_required
def logout_view(request):
    logout(request)
    
    return redirect('home')

