from django import forms
from django.contrib.auth import get_user_model
from .models import monitor
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class LoginForm(forms.ModelForm):
    class Meta:
        model = monitor
        fields = ["email", "password"]

class SignupForm(forms.ModelForm):
    class Meta:
        model = monitor
        fields = ["email", "fullname", "password"]