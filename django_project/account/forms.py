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
    admin = "admin"
    courier = "courier"
    sender = "sender"
    drop_pick_zone = "drop_pick_zone"
    

    ROLE_CHOICES = [
        (admin, "admin"),
        (courier, "courier"),
        (sender, "sender"),
        (drop_pick_zone, "drop pick zone")
    ]

    role = forms.ChoiceField(
        required=True,
        choices=ROLE_CHOICES,
        widget=forms.RadioSelect(attrs={'id': 'id_role'}),
    )

    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "name"
            }
        )
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

    tag = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "tag"
            }
        )
    )



    class Meta:
        model = User
        fields = ('name', 'username', 'email', 'password1', 'password2', 'role', 'tag')

class PackageForm(forms.ModelForm):
    
    class Meta:
        model = Package
        fields = ['packageName', 'deliveryType', 'dropOffLocation', 'packageDescription', 'recipientName', 'recipientAddress', 'sendersAddress', 'recipientEmail', 'recipientTelephone']
        widgets = {
            'packageName': forms.TextInput(attrs={'class': 'form-control'}),
            'deliveryType': forms.TextInput(attrs={'class': 'form-control'}),
            'dropOffLocation': forms.TextInput(attrs={'class': 'form-control'}),
            'packageDescription': forms.TextInput(attrs={'class': 'form-control'}),
            'recipientName': forms.TextInput(attrs={'class': 'form-control'}),
            'recipientEmail': forms.TextInput(attrs={'class': 'form-control'}),
            'recipientTelephone': forms.TextInput(attrs={'class': 'form-control'}),
            'recipientAddress': forms.TextInput(attrs={'class': 'form-control'}),
            'sendersAddress': forms.TextInput(attrs={'class': 'form-control'}),
        }

class WarehouseForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'phone', 'address', 'tag']

class DropPickForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'phone', 'address', 'tag', 'warehouse']
