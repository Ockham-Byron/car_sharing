from django.urls import path

from .views import *

urlpatterns = [
    path('<id>/mask', not_show_view, name='not_show'),
    
   
]