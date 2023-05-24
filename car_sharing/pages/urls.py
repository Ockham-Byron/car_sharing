from django.urls import path

from .views import *

urlpatterns = [
    path('', home_page_view, name='home'),
    path('dashboard', dashboard_view, name='dashboard'),

    #legals
    path('privacy-policy', privacy_policy_view, name='privacy_policy'),
    path('terms-conditions', terms_conditions_view, name='terms_conditions'),
]