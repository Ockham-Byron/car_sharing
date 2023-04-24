from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    register_user = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'register_user')

class CustomUserLoginForm(forms.Form):
    login_user = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    email = forms.CharField(max_length=255, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(max_length=255, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    class Meta:
        model = CustomUser
        fields = ('email', 'login_user', 'password')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')