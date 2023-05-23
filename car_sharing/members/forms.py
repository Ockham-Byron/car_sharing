from django import forms
from django.utils.translation import gettext_lazy as _

from django.core.exceptions import ValidationError 
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    register_user = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    username = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': _('Courriel')}))
    email = forms.CharField(max_length=255, widget=forms.EmailInput(attrs={'placeholder': _('Courriel')}))
    password1 = forms.CharField(max_length=255, widget=forms.PasswordInput(attrs={'placeholder': _('Mot de passe')}))
    password2 = forms.CharField(max_length=255, widget=forms.PasswordInput(attrs={'placeholder': _('Mot de passe bis')}))

    def email_clean(self):  
        email = self.cleaned_data['email'].lower()  
        new = CustomUser.objects.filter(email = email)  
        if new.count():  
            raise ValidationError(_("Un compte avec ce courriel existe déjà."))  
            
        return email  
    
    def clean_password2(self):  
        password1 = self.cleaned_data['password1']  
        password2 = self.cleaned_data['password2']  
  
        if password1 and password2 and password1 != password2:  
            raise ValidationError(_("Les mots de passe ne correspondent pas."))  
        return password2  
    
    def save(self, commit = True):  
        user = CustomUser.objects.create_user(  
            self.cleaned_data['username'],  
            self.cleaned_data['email'],  
            self.cleaned_data['password1']  
        )  
        return user 

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'register_user')

class CustomUserLoginForm(forms.Form):
    login_user = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    email = forms.CharField(max_length=255, widget=forms.EmailInput(attrs={'placeholder': _('Courriel')}))
    password = forms.CharField(max_length=255, widget=forms.PasswordInput(attrs={'placeholder': _('Mot de passe')}))

    class Meta:
        model = CustomUser
        fields = ('email', 'login_user', 'password')

class CustomUserChangeForm(UserChangeForm):
    username = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': _('Courriel'), 'class':"form-control"}))
    email = forms.CharField(max_length=255, widget=forms.EmailInput(attrs={'placeholder': _('Courriel'), 'class':"form-control"}))
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'avatar')