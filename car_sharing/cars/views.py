from django.shortcuts import render, redirect
from datetime import date
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from postit.models import PostIt, PostItNotShowed
from .models import *
from .forms import *
from members.models import CustomUser

@login_required
def car_detail_view(request, id, slug):
    car = Car.objects.get(id=id)
    users = car.users.all()
    insurance_price = 0
    insurance = None

    #Insurance
    if Insurance.objects.filter(car=car).exists():
        insurance = Insurance.objects.get(car=car)
        insurance_price = insurance.price
    


    car_paid_by=None
    if PurchaseParticipation.objects.filter(car=car).exists():
        car_paid_by = PurchaseParticipation.objects.filter(car=car)


    energy_by_user = []
    for user in users:
        if Energy.objects.filter(car = car, paid_by=user).exists():
            user_energy_bills = Energy.objects.filter(car=car, paid_by=user)
            total_energy_bill_user = 0
            for energy_bill in user_energy_bills:
                total_energy_bill_user += energy_bill.price
            energy_bills = ({'user': user, 'total_energy_bill_user': total_energy_bill_user})
            energy_by_user.append(energy_bills)
        
    
    total_energy = 0
    for i in energy_by_user:
        total_energy += i['total_energy_bill_user']

    repairs_by_user = []
    for user in users:
        if Repair.objects.filter(car = car, paid_by=user).exists():
            user_repair_bills = Repair.objects.filter(car=car, paid_by=user)
            total_repair_bill_user = 0
            for repair_bill in user_repair_bills:
                total_repair_bill_user += repair_bill.price
            repair_bills = ({'user': user, 'total_repair_bill_user': total_repair_bill_user})
            repairs_by_user.append(repair_bills)

    total_repairs = 0
    for i in repairs_by_user:
        total_repairs += i['total_repair_bill_user']

    totals_paid_by_user = []
    for user in users:
        paid_by_user = 0
        if PurchaseParticipation.objects.filter(car = car, user = user).exists():
            user_participation = PurchaseParticipation.objects.filter(car = car, user = user)
            for i in user_participation:
                paid_by_user += i.price_paid
        if InsuranceParticipation.objects.filter(insurance = insurance, user = user).exists():
            user_insurance = InsuranceParticipation.objects.filter(insurance = insurance, user = user)
            for i in user_insurance:
                paid_by_user += i.price_paid
        if Energy.objects.filter(car=car, paid_by = user).exists():
            user_energy_paid = Energy.objects.filter(car = car, paid_by = user)
            for i in user_energy_paid:
                paid_by_user += i.price
        if Repair.objects.filter(car=car, paid_by = user).exists():
            user_repairs_paid = Repair.objects.filter(car = car, paid_by = user)
            for i in user_repairs_paid:
                paid_by_user += i.price
        resume_paid_by_user = ({'user':user, 'paid_by_user':paid_by_user})
        totals_paid_by_user.append(resume_paid_by_user)

    total_charges = 0
    for i in totals_paid_by_user:
        total_charges += i['paid_by_user']

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

    #Postit
    post_its = None
    
    if PostIt.objects.filter(car=car).exists():
        post_its = PostIt.objects.filter(car=car)
        for post_it in post_its:
            if PostItNotShowed.objects.filter(post_it = post_it, user= request.user).exists():
                print("True")
                print(post_it.id)
                post_its = post_its.exclude(id = post_it.id)


    #Reservations
    reservations = None
    if Reservation.objects.filter(car=car).exists():
        reservations = Reservation.objects.filter(car=car)
    

    context={
        'car': car,
        'insurance': insurance,
        'insurance_price': insurance_price,
        'total_charges': total_charges,
        'totals_paid_by_user': totals_paid_by_user,
        'car_paid_by': car_paid_by,
        'nb_km_total': nb_km_total,
        'total_energy': total_energy,
        'energy_by_user': energy_by_user,
        'repairs_by_user': repairs_by_user,
        'total_repairs': total_repairs,
        'trips_by_user': trips_by_user,
        'post_its':post_its,
        'reservations':reservations,
    }

    return render(request, 'cars/car_detail.html', context=context)

@login_required
def costs_detail_view(request, slug, id):
    car = Car.objects.get(id=id)
    users = car.users.all()

    car_paid_by=None
    if PurchaseParticipation.objects.filter(car=car).exists():
        car_paid_by = PurchaseParticipation.objects.filter(car=car)
    
    # Insurances
    all_insurances = None
    insurances = None
    current_insurance = None
    is_more_insurances = False
    insurances_by_user = []
    if Insurance.objects.filter(car=car).exists():
        all_insurances = Insurance.objects.filter(car=car)
        insurances = all_insurances.order_by('renewal_date')[:3]
        latest_insurance = all_insurances.latest('renewal_date')
        if latest_insurance.renewal_date > date.today():
            current_insurance = latest_insurance
        for user in users:
            for insurance in insurances:
                if InsuranceParticipation.objects.filter(insurance = insurance, user = user).exists():
                    insurances_paid_by_user = InsuranceParticipation.objects.filter(insurance = insurance, user = user)
                    for i in insurances_paid_by_user:
                        insurance_paid_by_user = ({'insurance':i.insurance, 'user':user, 'price_paid':i.price_paid})
                        insurances_by_user.append(insurance_paid_by_user)
    
    
        if all_insurances.count() > 3:
            is_more_insurances = True

    #Energy
    all_energy = None
    if Energy.objects.filter(car = car).exists():
        all_energy = Energy.objects.filter(car=car)

    energy_by_user = []
    for user in users:
        if Energy.objects.filter(car=car, paid_by = user).exists():
            total_paid = 0
            energy_bills_user = Energy.objects.filter(car=car, paid_by=user)
            for bill in energy_bills_user:
                total_paid += bill.price
            energy_bill_user = ({'total_paid': total_paid, 'user':user})
            energy_by_user.append(energy_bill_user)


    #Repairs
    all_repairs = None
    if Repair.objects.filter(car=car).exists():
        all_repairs = Repair.objects.filter(car=car)

    repair_by_user = []
    for user in users:
        if all_repairs != None:
            if all_repairs.filter(paid_by=user).exists():
                total_paid = 0
                repair_bills_user = all_repairs.filter(paid_by = user)
                for bill in repair_bills_user:
                    total_paid += bill.price
                repair_bill_user = ({'total_paid': total_paid, 'user':user})
                repair_by_user.append(repair_bill_user)

    
    


    context = {
        'car': car,
        'users': users,
        'car_paid_by': car_paid_by,
        'insurances': insurances,
        'current_insurance': current_insurance,
        'insurances_by_user':insurances_by_user,
        'is_more_insurances' : is_more_insurances,
        'all_energy':all_energy,
        'energy_by_user':energy_by_user,
        'all_repairs':all_repairs,
        'repair_by_user': repair_by_user,
    }

    return render(request, 'cars/charges_detail.html', context=context)

@login_required
def trips_detail_view(request, id, slug):
    car = Car.objects.get(id=id)
    users = car.users.all()

    trips = None
    trips_by_user = []
    if Trip.objects.filter(car=car).exists():
        trips = Trip.objects.filter(car=car).order_by('-end')

    for user in users:
        if trips != None:
            if trips.filter(user=user).exists():
                total_trips_by_user = trips.filter(user=user)
                nb_trips_by_user = 0
                nb_km_by_user = 0
                for trip in total_trips_by_user:
                    nb_trips_by_user += 1
                    nb_km = trip.nb_km_end - trip.nb_km_start
                    nb_km_by_user += nb_km
                trips_user = ({'user': user, 'nb_trips_by_user': nb_trips_by_user, 'nb_km_by_user':nb_km_by_user})
                trips_by_user.append(trips_user)

    context = {
    'car': car,
    'users': users,
    'trips':trips,
    'trips_by_user': trips_by_user
}
    return render(request, 'cars/trips_detail.html', context=context)

@login_required
def add_car_view(request):
    form = AddCarForm()
    
    user= request.user
    if request.method == 'POST':
        form = AddCarForm(request.POST, request.FILES)
        
        
        if  form.is_valid():
            car = form.save()
            
            car.users.add(user)
            car.save()
            
            messages.success(request, f'Véhicule {car.name} est bien rentré au garage', extra_tags='Parfait !')
            return redirect('dashboard')

    return render(request, 'cars/forms/add_car_form.html', {'form': form,})