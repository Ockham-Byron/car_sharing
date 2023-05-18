from django.urls import path

from .views import *

urlpatterns = [
    path('car_detail/<slug:slug>', car_detail_view, name='car_detail'),
    path('<slug:slug>/costs', costs_detail_view, name='costs_detail'),
    path('<slug:slug>/trips', trips_detail_view, name='trips_detail'),

    #edit cars
    path('add-car', add_car_view, name='add_car'),
    path('<id>/add_purchase_parts', first_update_car_participations, name='add_car_participation'),
    path('<id>/update_car', update_car_view, name='update_car'),
    path('<id>/update_contribution', update_car_participation, name='update_car_participation'),
    
    
    
    #join car
    path('<id>/invitation', invitation_view, name='invitation'),
    path('join-car', join_car_view, name='join_car'),

    #reservations and trips
    path('<id>/reservation', add_reservation_view, name='add_reservation'),
    path('<id>/add-trip', add_trip_view, name='add_trip'),
    path('<id>/update-trip', update_trip_view, name='update_trip'),

    #charges
    path('<id>/create/', insurance_create_view, name='create_insurance'),
    path('<id>/add_insurance_parts', first_update_insurance_participations, name='add_insurance_participation'),
    path('<id>/update/', insurance_update_view, name='update_insurance'),
    path('<id>/update_insurance_contribution', update_insurance_participation, name='update_insurance_participation'),
    path('<id>/charges/add-energy', add_energy_view, name='add_energy'),
    path('<id>/charges/update-energy', update_energy_view, name='update_energy'),
    path('<id>/charges/add-repair', add_repair_view, name='add_repair'),
    path('<id>/charges/udpate-repair', update_repair_view, name='update_repair'),
]