from django.urls import path

from .views import *

urlpatterns = [
    path('car_detail/<id>/<slug:slug>', car_detail_view, name='car_detail'),
    path('<slug:slug>/<id>/costs', costs_detail_view, name='costs_detail'),
    path('<slug:slug>/<id>/trips', trips_detail_view, name='trips_detail'),

    #edit cars
    path('add-car', add_car_view, name='add_car'),
    path('<id>/add_purchase_parts', first_update_car_participations, name='add_car_participation'),
    
    
    
    #join car
    path('<id>/invitation', invitation_view, name='invitation'),
    path('join-car', join_car_view, name='join_car'),

    #reservations
    path('<id>/reservation', add_reservation_view, name='add_reservation'),

    #charges
    path('<id>/create/', insurance_create_view, name='create_insurance'),
    path('<id>/add_insurance_parts', first_update_insurance_participations, name='add_insurance_participation'),
    path('<id>/charges/add-charge', add_energy_view, name='add_energy'),
]