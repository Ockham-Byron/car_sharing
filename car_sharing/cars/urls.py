from django.urls import path

from .views import *

urlpatterns = [
    path('car_detail/<id>/<slug:slug>', car_detail_view, name='car_detail'),
    path('<slug:slug>/<id>/costs', costs_detail_view, name='costs_detail'),
    path('<slug:slug>/<id>/trips', trips_detail_view, name='trips_detail'),

    #edit cars
    path('add-car', add_car_view, name='add_car'),
    path('<id>/add-insurance', add_insurance_view, name='add_insurance'),
    path('<id:car_id>/<id:insurance_id>/insurance_parts', add_insurance_participation_view, name='add_insurance_participation'),

    #join car
    path('<id>/invitation', invitation_view, name='invitation'),
    path('join-car', join_car_view, name='join_car'),
   
]