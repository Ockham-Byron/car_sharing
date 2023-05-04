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

    class Meta:
        model = Car
        fields = ['name']