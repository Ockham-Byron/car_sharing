from django import forms
from django.forms import inlineformset_factory
from django.forms.utils import flatatt
from django.utils.translation import gettext_lazy as _
from .models import *
from members.models import CustomUser

class ReadOnlyWidget(forms.Widget):
    def render(self, name, value, attrs):
        final_attrs = self.build_attrs(attrs, name=name)
        if hasattr(self, 'initial'):
            value = self.initial
        return "%s" % (flatatt(final_attrs), value or '')
    
    def _has_changed(self, initial, data):
        return False


class ReadOnlyField(forms.FileField):
    widget = ReadOnlyWidget
    def __init__(self, widget=None, label=None, initial=None, help_text=None):
        forms.Field.__init__(self, label=label, initial=initial, 
            help_text=help_text, widget=widget)
    
    def clean(self, value, initial):
        self.widget.initial = initial
        return initial

class DateInput(forms.DateTimeInput):
    input_type = 'date'


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

class AddPurchaseParticipationForm(forms.ModelForm):

    price_paid = forms.FloatField(
                            required=True,
                            widget=forms.NumberInput(attrs={'placeholder': _('vous pourrez modifier'),
                                                        'class': 'form-control'
                                }))

    class Meta:
        model = PurchaseParticipation
        fields = ['price_paid']

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
    

    renewal_date = forms.DateField(widget=DateInput(format=('%Y-%m-%d'),
                                                    attrs={'class': 'form-control', 'type':'date'},
                                                    ),
                            required=True,
                            )
    class Meta:
        model = Insurance
        fields = ['company', 'price', 'renewal_date']

class InsuranceParticipationForm(forms.ModelForm):
   
    price_paid = forms.FloatField(
                            required=True,
                            widget=forms.NumberInput(attrs={'placeholder': _(''),
                                                        'class': 'form-control'
                                }))
    
    class Meta:
        model = InsuranceParticipation
        fields = [  'price_paid']

 

class AddReservationForm(forms.ModelForm):
    
    

    reservation_start = forms.DateField(widget=DateInput(format=('%Y-%m-%d'),
                                                    attrs={'class': 'form-control', 'type':'date'},
                                                    ),
                            required=True,
                            )

    reservation_end = forms.DateField(widget=DateInput(format=('%Y-%m-%d'),
                                                    attrs={'class': 'form-control', 'type':'date'},
                                                    ),
                            required=True,
                            )
    
    class Meta:
        model = Reservation
        fields = ['reservation_start', 'reservation_end']

class AddTripForm(forms.ModelForm):
    
    nb_km_start = forms.FloatField(
                            required=True,
                            widget=forms.NumberInput(attrs={'placeholder': _('voir sur le tableau de bord'),
                                                        'class': 'form-control'
                                }))
    
    nb_km_end = forms.FloatField(
                            required=True,
                            widget=forms.NumberInput(attrs={'placeholder': _("voir sur le tableau de bord"),
                                                        'class': 'form-control'
                                }))

    start = forms.DateField(widget=DateInput(format=('%Y-%m-%d'),
                                                    attrs={'class': 'form-control', 'type':'date'},
                                                    ),
                            required=True,
                            )

    end = forms.DateField(widget=DateInput(format=('%Y-%m-%d'),
                                                    attrs={'class': 'form-control', 'type':'date'},
                                                    ),
                            required=True,
                            )
    
    class Meta:
        model = Trip
        fields = [ 'start', 'end', 'nb_km_start', 'nb_km_end']


class AddEnergyForm(forms.ModelForm):
    energy_choices = Energy._meta.get_field('type_energy').choices
    
    type_energy = forms.ChoiceField(choices=energy_choices, required=None)
    
    price = forms.FloatField(
                            required=True,
                            widget=forms.NumberInput(attrs={'placeholder': _('prix'),
                                                        'class': 'form-control'
                                }))
    
    quantity = forms.FloatField(
                            required=True,
                            widget=forms.NumberInput(attrs={'placeholder': _('combien de litres, de kw, etc ?'),
                                                        'class': 'form-control'
                                }))
    
    

    paid_day = forms.DateField(widget=DateInput(format=('%Y-%m-%d'),
                                                    attrs={'class': 'form-control', 'type':'date'},
                                                    ),
                            required=True,
                            )
    
    class Meta:
        model = Energy
        fields = ['price', 'quantity', 'paid_by', 'paid_day', 'type_energy']

class AddRepairForm(forms.ModelForm):
    repair_choices = Repair._meta.get_field('type_repair').choices
    
    type_repair = forms.ChoiceField(choices=repair_choices, required=False)
    
    price = forms.FloatField(
                            required=True,
                            widget=forms.NumberInput(attrs={'placeholder': _('prix'),
                                                        'class': 'form-control'
                                }))
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': _('courte description'),
                                                              'class': 'form-control',
                                                              "rows":2, "cols":20
                                                              
                            }))
    
    

    paid_day = forms.DateField(widget=DateInput(format=('%Y-%m-%d'),
                                                    attrs={'class': 'form-control', 'type':'date'},
                                                    ),
                            required=True,
                            )
    class Meta:
        model = Repair
        fields = ['type_repair', 'price', 'paid_day','paid_by', 'description']




    

    
