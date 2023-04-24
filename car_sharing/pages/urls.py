from django.urls import path

from .views import *

urlpatterns = [
    path('', home_page_view, name='home'),
    path('dashboard', dashboard_view, name='dashboard')
]