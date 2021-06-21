from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


class popularStockForm(forms.ModelForm):
    class Meta:
        model = PopularStock
        fields = ('name', 'symbol')

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Username",
                "class": "text"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password",
                "class": "text"
            }
        ))

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder" : "Username",
                "class": "text"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder" : "Email",
                "class": "text"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Password",
                "class": "text"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder" : "Confirm Password",
                "class": "text"
            }
        ))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')



class portfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ('balance', 'user')


class holdingsForm(forms.ModelForm):
    class Meta:
        model = holdings
        fields = ('name', 'symbol', 'quantity', 'user')



class transactionsForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('name', 'symbol', 'quantity', 'type',  'price' , 'balance_before', 'balance_after', 'user')