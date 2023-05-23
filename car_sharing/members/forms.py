from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    register_user = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    email = forms.CharField(max_length=255, widget=forms.EmailInput(attrs={'placeholder': _('Courriel')}))
    password1 = forms.CharField(max_length=255, widget=forms.PasswordInput(attrs={'placeholder': _('Mot de passe')}))
    username = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': _('Courriel')}))
    password2 = forms.CharField(max_length=255, widget=forms.PasswordInput(attrs={'placeholder': _('Mot de passe bis')}))

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'register_user')

class CustomUserLoginForm(forms.Form):
    login_user = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    email = forms.CharField(max_length=255, widget=forms.EmailInput(attrs={'placeholder': _('Courriel')}))
    password = forms.CharField(max_length=255, widget=forms.PasswordInput(attrs={'placeholder': _('Mot de passe')}))

    class Meta:
        model = CustomUser
        fields = ('email', 'login_user', 'password')

class CustomUserChangeForm(UserChangeForm):
    username = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': _('Courriel')}))
    email = forms.CharField(max_length=255, widget=forms.EmailInput(attrs={'placeholder': _('Courriel')}))
    password1 = forms.CharField(max_length=255, widget=forms.PasswordInput(attrs={'placeholder': _('Mot de passe')}))
    
    password2 = forms.CharField(max_length=255, widget=forms.PasswordInput(attrs={'placeholder': _('Mot de passe bis')}))

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password')