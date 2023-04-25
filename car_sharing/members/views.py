from django.utils.translation import gettext as _
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, _("Descente du véhicule effective"))
    return redirect('home')
