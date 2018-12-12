from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(max_length=20,\
                widget=forms.TextInput(attrs={'class': 'form-control'}),\
                label='Display Name')
    username = forms.SlugField(max_length=15,\
                    widget=forms.TextInput(attrs={'class': 'form-control'}),\
                    label='Username:')
    password = forms.SlugField(max_length=15,\
           widget=forms.PasswordInput(attrs={'class': 'form-control'}),\
           label='Password:')
    class Meta:
        model  = User
        fields = ('first_name', 'username', 'password')

class LoginForm(forms.ModelForm):
    username = forms.SlugField(max_length=15,\
                    widget=forms.TextInput(attrs={'class': 'form-control mr-sm-2'}),\
                    label='Username:')
    password = forms.SlugField(max_length=15,\
           widget=forms.PasswordInput(attrs={'class': 'form-control mr-sm-2'}),\
           label='Password:')
    class Meta:
        model  = User
        fields = ('username', 'password')

class SettingsForm(forms.ModelForm):
    first_name = forms.CharField(max_length=20,\
                widget=forms.TextInput(attrs={'class': 'form-control'}),\
                label='Display Name')
    password = forms.SlugField(max_length=15,\
           widget=forms.PasswordInput(attrs={'class': 'form-control mr-sm-2'}),\
           label='Password:')
    class Meta:
        model  = User
        fields = ('first_name', 'password')

class SearchForm(forms.Form):
    search = forms.CharField(max_length=20,\
                widget=forms.TextInput(attrs={'class': 'form-control'}),\
                label='Search')

