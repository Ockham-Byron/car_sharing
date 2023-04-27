from django.urls import path

from .views import *

urlpatterns = [
    path('car_detail/<id>/<slug:slug>', car_detail_view, name='car_detail'),
    path('<slug:slug>/<id>/costs', costs_detail_view, name='costs_detail'),
   
]