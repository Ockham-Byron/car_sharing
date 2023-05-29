from django import forms

from django.utils.translation import gettext_lazy as _
from .models import *


class AddPostItForm(forms.ModelForm):

   
    
    message = forms.CharField(max_length=100, 
                                required=True,
                                widget=forms.Textarea(attrs={'placeholder': _('votre message...'),
                                                            'class': 'form-control'
                                    }))
    
    
    
    
    
    class Meta:
        model = PostIt
        fields = ['message']