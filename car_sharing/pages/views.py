from django.utils.translation import gettext as _
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView
from members.forms import *
from cars.models import Car

# Create your views here.
def home_page_view(request):
   
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        login_form = CustomUserLoginForm()
        signup_form = CustomUserCreationForm()
        
        context= {
            'login_form': login_form,
            'signup_form': signup_form,
        }

        if request.method == 'POST':
            print("Form pris en compte")
            if 'login_user' in request.POST:
                print("form_login_user")
                login_form = CustomUserLoginForm(request.POST)
                if login_form.is_valid():
                    print("form is valid")
                    email = request.POST.get('email')
                    password = request.POST.get('password')
                    user=authenticate(username = email, password = password )
                    if user is not None:
                        print("on login success")
                        login(request, user)
                        return redirect('dashboard')
                    else:
                        print("user no")
                else:
                    print(login_form.errors.as_data())
            else:
                print("pas login_user")
            
            if 'register_user' in request.POST:
                
                print("form_register_user")
                signup_form=CustomUserCreationForm(request.POST)
                if signup_form.is_valid():
                    print("form is valid")
                    signup_form.save()
                    email = signup_form.cleaned_data['email']
                    password = signup_form.cleaned_data['password1']
                    user = authenticate(username = email, password = password)
                    login(request, user)
                    return redirect('dashboard')
                    
                else:
                    print(signup_form.errors.as_data())


        else:
            print("marche pas.")
        return render(request, 'home.html', context=context)

def dashboard_view(request):
    cars = Car.objects.filter(users__id__contains = request.user.id)
    
    if cars.count() > 1:
        context = {
            'cars': cars,
        }
        return render(request, 'dashboard.html', context=context)
    else:
        car = Car.objects.get(users__id__contains = request.user.id)
        return redirect('car_detail', car.id, car.slug)
