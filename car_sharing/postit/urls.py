from django.urls import path

from .views import *

urlpatterns = [
    path('<id>/mask', not_show_view, name='not_show'),
    path('<id>/delete', delete_modal_view, name='delete_modal'),
    path('<id>/delete/for_everyone', delete_postit_for_everyone, name='delete_postit_for_everyone'),
   
]