from django import forms
from django.utils.translation import gettext_lazy as _
from .models import *



class AddCarForm(forms.ModelForm):
    energy_choices = Car._meta.get_field('energy').choices
    
    name = forms.CharField(max_length=100, 
                                required=True,
                                widget=forms.TextInput(attrs={'placeholder': _('la marque, un surnom...'),
                                                            'class': 'form-control'
                                    }))
    
    immatriculation = forms.CharField(max_length=100, 
                                required=False,
                                widget=forms.TextInput(attrs={'placeholder': _('pas obligatoire, hein'),
                                                            'class': 'form-control'
                                    }))
    
    price = forms.FloatField(
                            required=True,
                            widget=forms.NumberInput(attrs={'placeholder': _('vous pourrez modifier'),
                                                        'class': 'form-control'
                                }))
    
    energy = forms.ChoiceField(choices=energy_choices)

    nb_users = forms.IntegerField(
                            required=True,
                            widget=forms.NumberInput(attrs={'placeholder': _('oui, combien ?'),
                                                        'class': 'form-control'
                                }))
    
    class Meta:
        model = Car
        fields = ['name', 'immatriculation', 'price', 'energy', 'nb_users']

class AddInsuranceForm(forms.ModelForm):
    
    company = forms.CharField(max_length=100, 
                                required=True,
                                widget=forms.TextInput(attrs={'placeholder': _('où le véhicule est-il assuré ?'),
                                                            'class': 'form-control'
                                    }))
    
    price = forms.FloatField(
                            required=True,
                            widget=forms.NumberInput(attrs={'placeholder': _('prix total'),
                                                        'class': 'form-control'
                                }))
    

    renewal_date = forms.DateField(widget=forms.SelectDateWidget(attrs={'class': 'date-select'}),
                            required=True,
                            )
    
    class Meta:
        model = Insurance
        fields = ['company', 'price', 'renewal_date']

class AddInsuranceParticipationForm(forms.ModelForm):
    user = forms.ChoiceField( widget=forms.CheckboxInput(attrs={'class': 'check-abstract'}), choices=CustomUser.objects.none())
    price_paid = forms.FloatField(
                            required=True,
                            widget=forms.NumberInput(attrs={'placeholder': _('vous pourrez modifier'),
                                                        'class': 'form-control'
                                }))
    
    class Meta:
        model = InsuranceParticipation
        fields = ['user', 'price_paid']

    def __init__(self, car, *args, **kwargs):
        super(AddInsuranceParticipationForm, self).__init__(*args, **kwargs)
        
        
        self.fields['user'].choices=car.users.all()

    