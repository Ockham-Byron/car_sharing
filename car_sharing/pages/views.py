import sweetify
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
            
            if 'login_user' in request.POST:
                
                login_form = CustomUserLoginForm(request.POST)
                if login_form.is_valid():
                    
                    email = request.POST.get('email')
                    password = request.POST.get('password')
                    user=authenticate(username = email, password = password )
                    if user is not None:
                        login(request, user)
                        return redirect('dashboard')
                    else:
                        if CustomUser.objects.filter(email=email).exists():
                            sweetify.warning(request, _('Attention'), text= _('Le mot de passe ne correspond pas à ce courriel.'))
                        else:
                            sweetify.warning(request, _('Attention'), text= _('Aucun utilisateur enregistré avec ce courriel.'))
                
           
            
            if 'register_user' in request.POST:
                print('register_user')
                signup_form=CustomUserCreationForm(request.POST)
                
                if signup_form.is_valid():
                    signup_form.save()
                    email = signup_form.cleaned_data['email']
                    password = signup_form.cleaned_data['password1']
                    user = authenticate(username = email, password = password)
                    login(request, user)
                    return redirect('dashboard')
                else:
                    list_errors = [(k, v[0]) for k, v in signup_form.errors.items()]
                    errors = tuple(list_errors)
                    message = errors[0][1]
                    print(errors[0][1])
                
                    sweetify.warning(request, _('Attention'), text= message, persistent='Ok')
                

        return render(request, 'home.html', context=context)

def dashboard_view(request):
    cars = None
    
    if Car.objects.filter(users__id__contains=request.user.id).exists():
        cars = Car.objects.filter(users__id__contains = request.user.id)
    
        if cars.count() == 1:
            car = Car.objects.get(users__id__contains = request.user.id)
            return redirect('car_detail',  car.slug)
    
    context = {
                'cars': cars,
            }
    
    
    return render(request, 'dashboard.html', context=context)

def privacy_policy_view(request):
    return render(request, 'legals/privacy_policy.html',)

def terms_conditions_view(request):
    return render(request, 'legals/terms_conditions.html',)