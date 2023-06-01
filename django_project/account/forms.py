from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .models import Package

class LoginForm(forms.Form):
    username = forms.CharField(
        widget= forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "username"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "password"
            }
        )
    )


class SignUpForm(UserCreationForm):
    courier = "courier"
    sender = "sender"
    recipient = "recipient"

    ROLE_CHOICES = [
        (courier, "courier"),
        (sender, "sender"),
        (recipient, "recipient")
    ]

    role = forms.ChoiceField(
        required=True,
        choices=ROLE_CHOICES,
        widget=forms.RadioSelect,
    )

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "username"
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "password"
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "confirm password"
            }
        )
    )
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "email"
            }
        )
    )

    # role = forms.ChoiceField(
    #             choices = ROLE_CHOICES,
    #             required = True,
    #             widget = forms.Select(attrs = {'class': 'control--checkbox', 'placeholder': ''}),
    #             )
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'role')
        
class PackageForm(forms.ModelForm):
        widgets = {
            'packageName': forms.TextInput(attrs={'class': 'form-control'}),
            'packageDescription': forms.TextInput(attrs={'class': 'form-control'}),
            'recipientName': forms.TextInput(attrs={'class': 'form-control'}),
            'recipientAddress': forms.TextInput(attrs={'class': 'form-control'}),
            'sendersAddress': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

        class Meta:
            model = Package
            fields = ['packageName', 'packageDescripton', 'recipientName', 'recipientAddress', 'sendersAddress']

# class PackageForm(forms.ModelForm):
#     class Meta:
#         model = Package
#         fields = ['packageName', 'packageDescripton', 'recipientName', 'recipientAddress', 'sendersAddress']