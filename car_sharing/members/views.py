from django.utils.translation import gettext as _
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from members.forms import CustomUserChangeForm
from .models import *
from cars.models import Car, Reservation, Trip, PurchaseParticipation, Insurance, InsuranceParticipation, Energy, Repair

@login_required
def profile_view(request, id):
    user = CustomUser.objects.get(id=id)
    cars = Car.objects.filter(users__id__contains=user.id)
    car = None
    if len(cars) == 1:
        car = cars[0]

    reservations = None
    reservations_to_confirm = None
    waiting_reservations = None
    for car in cars:
        if Reservation.objects.filter(car=car).exists():
            reservations = Reservation.objects.filter(car=car)
            reservations_to_confirm = reservations.filter(status = "pending").exclude(user=user)
            waiting_reservations = reservations.filter(status="pending", user=user)

    trips = None
    user_trips = None
    nb_kms = 0
    for car in cars:
        if Trip.objects.filter(car=car).exists():
            trips = Trip.objects.filter(car=car)
            user_trips = trips.filter(user=user)
            for user_trip in user_trips:
                trip_nb_km = user_trip.nb_km_end - user_trip.nb_km_start
                nb_kms += trip_nb_km

    charges = 0
    purchase_part = 0
    insurance_part = 0
    energy = 0
    repair = 0
    for car in cars:
        if PurchaseParticipation.objects.filter(car=car).exists():
            purchase_parts = PurchaseParticipation.objects.filter(car=car)
            if purchase_parts.filter(user=user).exists():
                user_purchase_part = purchase_parts.get(user=user)
                purchase_part = user_purchase_part.price_paid
        if Insurance.objects.filter(car=car).exists():
            insurances = Insurance.objects.filter(car=car)
            for i in insurances:
                if InsuranceParticipation.objects.filter(insurance = i).exists():
                    insurance_parts = InsuranceParticipation.objects.filter(insurance=i)
                    user_insurance_parts = insurance_parts.filter(user=user)
                    for i in user_insurance_parts:
                        insurance_part += i.price_paid
        if Energy.objects.filter(car=car).exists():
            energies = Energy.objects.filter(car=car)
            user_energies = energies.filter(paid_by=user)
            for i in user_energies:
                energy += i.price
        if Repair.objects.filter(car=car).exists():
            repairs = Repair.objects.filter(car=car)
            user_repairs = repairs.filter(paid_by=user)
            for i in user_repairs:
                repair += i.price


    
           

    charges = purchase_part + insurance_part + energy + repair

    ratio = 0
    if nb_kms != 0 and charges != 0:
        ratio = round(charges / nb_kms, 2)
    print(ratio)
    


    context = {
        'user': user,
        'car':car,
        'reservations': reservations,
        'reservations_to_confirm':reservations_to_confirm,
        'waiting_reservations':waiting_reservations,
        'user_trips': user_trips,
        'nb_kms':nb_kms,
        'charges':charges,
        'purchase_part':purchase_part,
        'insurance_part': insurance_part,
        'energy': energy,
        'repair':repair,
        'ratio':ratio,
        }
    
    return render(request, 'members/profile.html', context=context)
@login_required
def logout_view(request):
    logout(request)
    
    return redirect('home')

@login_required
def update_profile_view(request, id):
    user = CustomUser.objects.get(id=id);
    form = CustomUserChangeForm(instance = user)
    

    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user = form.save()
            return redirect('profile', user.id)

    return render(request, 'members/update_profile_form.html', {'form': form, 'user': user})

