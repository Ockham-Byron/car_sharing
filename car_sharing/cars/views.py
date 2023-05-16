from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from extra_views import UpdateWithInlinesView, InlineFormSetFactory
import uuid
import sweetify
import pytz
from django.forms import formset_factory
from django.views.generic import UpdateView, CreateView
from datetime import date, datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from postit.models import PostIt, PostItNotShowed
from .models import *
from .forms import *
from members.models import CustomUser
from postit.models import PostIt

utc = pytz.UTC


def check_reservation_availibility(start_date, end_date, car):
    qs = Reservation.objects.filter(
        reservation_start__gte = start_date,
        reservation_start__lte = end_date,
        reservation_end__gte = end_date, 
        car = car) or Reservation.objects.filter(
        reservation_start__lte = start_date,
        reservation_end__gte = start_date,
        reservation_end__lte = end_date,
        car = car) or Reservation.objects.filter(
        reservation_start__lte = start_date,
        reservation_end__gte = end_date,
        car = car)
    
    qs = qs.exclude(status = "cancelled")
    qs = qs.exclude(status = "rejected")

    if qs.exists():
        
        return False
    
    else:
        return True

@login_required
def car_detail_view(request, id, slug):
    car = Car.objects.get(id=id)
    users = car.users.all()
    last_insurance_price = 0
    last_insurance = None
    is_insurance_past = False
    
    

    #Insurance
    total_insurance = 0
    if Insurance.objects.filter(car=car).exists():
        insurances = Insurance.objects.filter(car=car)
        for i in insurances:
            total_insurance += i.price
        last_insurance = insurances.latest('renewal_date')
        last_insurance_price = last_insurance.price
        if last_insurance.renewal_date < date.today():
            is_insurance_past = True
    


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
        if last_insurance != None:
            insurances = Insurance.objects.filter(car=car)
            for insurance in insurances:
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
        'last_insurance': last_insurance,
        'last_insurance_price': last_insurance_price,
        'is_insurance_past': is_insurance_past,
        'total_insurance': total_insurance,
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
def invitation_view(request, id):
    car = Car.objects.get(id=id)
    context = {'car': car,}

    return render(request, 'cars/modals/invitation_modal.html', context=context)

@login_required
def add_car_view(request):
    form = AddCarForm()
    
    
    if request.method == 'POST':
        form = AddCarForm(request.POST, request.FILES)
        if  form.is_valid():
            car = form.save()
            car.users.add(request.user)
            car.save()
            
            participation = PurchaseParticipation(car=car, user=request.user, price_paid=0 )
            participation.save()
            messages.success(request, f'Véhicule {car.name} est bien rentré au garage', extra_tags='Parfait !')
            return redirect('dashboard')

    return render(request, 'cars/forms/add_car_form.html', {'form': form,})

@login_required
def first_update_car_participations(request, id):
    car = Car.objects.get(id=id)
    participations = PurchaseParticipation.objects.filter(car=car, first_complete=False)
    nb_to_edit = len(participations)
    participation = participations.all()[0]
    

    context = {
        'car':car,
        'participations':participations,
        'participation':participation,
        
        }
    
    if request.method == 'POST':
        price_paid = request.POST.get('price_paid')
        participation.price_paid = price_paid
        participation.first_complete = True
        participation.save()
        if nb_to_edit > 1:
            return redirect('add_car_participation', id)
        else:
            return redirect('car_detail', car.id, car.slug)

        
    
    print(nb_to_edit)

    return render(request, "cars/forms/first_update_car_participations.html", context=context)

@login_required
def update_car_view(request, id):
    car = Car.objects.get(id=id)
    form = AddCarForm(instance=car)
    paid_by = PurchaseParticipation.objects.filter(car=car)
    
    
    if request.method == 'POST':
        form = AddCarForm(request.POST, request.FILES, instance=car)
        if  form.is_valid():
            form.save()
        if 'update_car' in request.POST:
            messages.success(request, f'Véhicule {car.name} bien actualisé', extra_tags='Parfait !')
            return redirect('car_detail', car.id, car.slug)
        else:
            part_id = request.POST.get('participation')
            participation = PurchaseParticipation.objects.get(id=part_id)
            return redirect('update_car_participation', participation.id)
        

    return render(request, 'cars/forms/update_car_form.html', {'form': form, 'car': car, 'paid_by': paid_by})

@login_required
def update_car_participation(request, id):
    participation = PurchaseParticipation.objects.get(id=id)
    
    car = participation.car
    form = AddPurchaseParticipationForm(instance=participation)

    if request.method == 'POST':
        form = AddPurchaseParticipationForm(request.POST, instance=participation)
        if form.is_valid():
            form.save()
        return redirect('update_car', car.id)
    
    return render(request, 'cars/forms/update_car_participation_form.html', {'form': form, 'car': car, 'participation': participation})

@login_required
def join_car_view(request):
    
    if request.method == 'POST':
        car_code = request.POST.get('uuid')

        def is_valid_uuid(value):
            try:
                uuid.UUID(str(value))
                return True
            except ValueError:
                return False
        
        def car_exists(value):
            try:
                Car.objects.get(id=value)
                return True
            except Car.DoesNotExist:
                return False

        if is_valid_uuid(car_code):
            if car_exists(car_code):
                car = Car.objects.get(id=car_code)
                users = car.users.all()
                if request.user in users:
                    messages.error(request, f'Vous faites partie de ce groupe')
                else:
                    car.users.add(request.user)    
                    car.save()
                    participation = PurchaseParticipation(car=car, user=request.user, price_paid=0)
                    participation.save()
                    return redirect('dashboard')
            
            else:
                messages.error(request, f'Ce groupe non')
                

        else:
            messages.error(request, f'Invalide')
            

    return render(request, 'cars/forms/join_car.html')

@login_required
def insurance_create_view(request, id):
    car = Car.objects.get(id=id)
    form = AddInsuranceForm()
    formset = InsuranceParticipationFormSet
    users = car.users.all()

    context = {
        'form':form,
        'formset': formset,
    }

    if request.method == 'POST':
        form = AddInsuranceForm(request.POST)
        if  form.is_valid():
            insurance = form.save()
            insurance.car = car
            insurance.save()
            for user in users:
                participation = InsuranceParticipation(insurance= insurance, user=user, price_paid=0)
                participation.save()
            return redirect('add_insurance_participation', insurance.id)

    return render(request, "cars/forms/add_insurance_form.html", context=context)

@login_required
def first_update_insurance_participations(request, id):
    insurance = Insurance.objects.get(id=id)
    car = insurance.car
    participations = InsuranceParticipation.objects.filter(insurance=insurance, first_complete=False)
    nb_to_edit = len(participations)
    participation = participations.all()[0]
    

    context = {
        'insurance':insurance,
        'participations':participations,
        'participation':participation,
        
        }
    
    if request.method == 'POST':
        price_paid = request.POST.get('price_paid')
        participation.price_paid = price_paid
        participation.first_complete = True
        participation.save()
        if nb_to_edit > 1:
            return redirect('add_insurance_participation', id)
        else:
            return redirect('car_detail', car.id, car.slug)

        
    
    print(nb_to_edit)

    return render(request, "cars/forms/first_update_insurance_participations.html", context=context)

@login_required
def add_reservation_view(request, id):
    car = Car.objects.get(id=id)
    form = AddReservationForm()
    

    
    
    if request.method == 'POST':
        form = AddReservationForm(request.POST)
        if  form.is_valid():
            reservation = form
            start = reservation.instance.reservation_start
            start = start.replace(tzinfo=utc)
            
            reservation.instance.reservation_end_calendar = reservation.instance.reservation_end.date() + timedelta(days=1)
            reservation.instance.car = car
            reservation.instance.user = request.user
            if start < datetime.now().replace(tzinfo=utc):
                print ('problème')
                sweetify.warning(request, _('Attention'), text= _('La date de début est déjà passée'))
            elif reservation.instance.reservation_end < reservation.instance.reservation_start:
                sweetify.warning(request, _('Attention'), text= _('La date de fin est antérieure à la date de début'))
            else:
                availability = check_reservation_availibility(start_date=reservation.instance.reservation_start, end_date=reservation.instance.reservation_end, car=car)
                if availability == False:
                    sweetify.warning(request, _('Problème'), text=_('Véhicule déjà réservé à ces dates'), persistent="OK")
                else:
                    reservation = reservation.save()
                    start = reservation.reservation_start
                    end = reservation.reservation_end
                    post_it = PostIt()
                    post_it.car = car
                    post_it.sender = request.user
                    post_it.reservation = reservation
                    post_it.color = "#E28413"
                    post_it.message = _("J'ai réservé du " + start.strftime('%d-%m') + " au " + end.strftime('%d-%m')) 
                    post_it.save()
                    return redirect('car_detail', car.id, car.slug)
    

    return render(request, 'cars/forms/add_reservation_form.html', {'form': form, 'car': car})

@login_required
def add_energy_view(request, id):
    car = Car.objects.get(id=id)
    users = car.users.all()
    nb_users = len(users)
    form = AddEnergyForm()
    print(car.energy)

    if request.method == 'POST':
        form = AddEnergyForm(request.POST)
        if form.is_valid():
            if car.energy != "hybride rechargeable":
                type_energy = car.energy
            else:
                type_energy = request.POST.get('type_energy')
            if nb_users == 1:
                paid_by = request.user
            else:
                user_id = request.POST.get('paid_by')
                paid_by = CustomUser.objects.get(id = user_id)
            
            energy=form
            energy.save(commit=False)
            energy.instance.car = car
            energy.instance.paid_by = paid_by
            energy.instance.type_energy = type_energy
            energy.save()
            return redirect('costs_detail', car.slug, car.id)
    else:
        print(form.errors.as_data)



    context = {'form':form,
               'car': car,
               'users':users,
               'nb_users': nb_users}
    return render(request, 'cars/forms/add_energy_form.html', context=context)

@login_required
def add_repair_view(request, id):
    car = Car.objects.get(id=id)
    users = car.users.all()
    nb_users = len(users)
    form = AddRepairForm()
    

    if request.method == 'POST':
        form = AddRepairForm(request.POST)
        if form.is_valid():
            
            if nb_users == 1:
                paid_by = request.user
            else:
                user_id = request.POST.get('paid_by')
                paid_by = CustomUser.objects.get(id = user_id)
            
            repair=form
            repair = repair.save(commit=False)
            
            repair.car = car
            repair.paid_by = paid_by
            
            repair.save()
            return redirect('costs_detail', car.slug, car.id)
    else:
        print(form.errors.as_data)



    context = {'form':form,
               'car': car,
               'users':users,
               'nb_users': nb_users}
    return render(request, 'cars/forms/add_repair_form.html', context=context)