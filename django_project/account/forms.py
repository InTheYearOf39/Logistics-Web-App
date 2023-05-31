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
                "class": "form-control"
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
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