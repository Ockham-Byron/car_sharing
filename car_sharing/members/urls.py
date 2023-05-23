from django.urls import path
from .views import *

urlpatterns = [
    path('logout/', logout_view, name='logout'),
    path('<id>/profile/', profile_view, name='profile'),
    path('<id>/profile_update/', update_profile_view, name='update_profile'),
]