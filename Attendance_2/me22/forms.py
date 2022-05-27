from unicodedata import name
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class LoginForm(forms.Form):
    username = forms.CharField(
        widget= forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )


class SignUpForm(UserCreationForm):
    username = forms.CharField(label="ID ",
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password1 = forms.CharField(label="Password ",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password2 = forms.CharField(label="Confirm Password ",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    first_name = forms.CharField(label="Name ",
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    class Meta:
        model = User
        fields = ('username', 'first_name','password1', 'password2')

DATE_CHOICES = [tuple([x, x]) for x in range(1, 32)]
MONTH_CHOICES = [tuple([x, x]) for x in range(1, 13)]
YEAR_CHOICES = [tuple([x, x]) for x in range(2022,2025)]


class date_form(forms.Form):
    D = forms.IntegerField(
        label="Date ", widget=forms.Select(choices=DATE_CHOICES))
    M = forms.IntegerField(
        label="Month ", widget=forms.Select(choices=MONTH_CHOICES))
    Y = forms.IntegerField(
        label="Year ", widget=forms.Select(choices=YEAR_CHOICES))

class stud(forms.Form):
    name = forms.CharField(label="Roll No ", widget=forms.TextInput(
        attrs={'class': 'form-control'})) 