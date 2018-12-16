from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from .models import Dish

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
                label='Display Name', required=False)
    password = forms.SlugField(max_length=15,\
           widget=forms.PasswordInput(attrs={'class': 'form-control mr-sm-2'}),\
           label='Password:', required=False)
    class Meta:
        model  = User
        fields = ('first_name', 'password')

class SearchForm(forms.Form):
    search = forms.CharField(max_length=20,\
                widget=forms.TextInput(attrs={'class': 'form-control'}),\
                label='Search')

class NewRestaurant(forms.Form):
    name = forms.CharField(max_length=80,\
                widget=forms.TextInput(attrs={'class': 'form-control'}),\
                label='Restaurant Name')
    lat = forms.FloatField(required=True, max_value=100, min_value=-100, 
        widget=forms.NumberInput()) 

    long = forms.FloatField(required=True, max_value=100, min_value=-100, 
        widget=forms.NumberInput()) 

class NewDish(forms.Form):
    name = forms.CharField(max_length=200,\
                widget=forms.TextInput(attrs={'class': 'form-control input-field col s12'}),\
                label='Name')
    dish_type = forms.CharField(max_length=100,\
                widget=forms.TextInput(attrs={'class': 'form-control input-field col s12'}),\
                label='Type')
    allergens = forms.CharField(max_length=200,\
                widget=forms.TextInput(attrs={'class': 'form-control input-field col s12'}),\
                label='Allergens')
    price = forms.FloatField(required=True, max_value=200, min_value=0,
        widget=forms.NumberInput()) 

    class Meta:
        model = Dish 
        fields = ['name', 'dish_type', 'allergens', 'price']



