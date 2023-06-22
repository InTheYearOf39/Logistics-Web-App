from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .models import Package
from django.contrib.auth import password_validation
from django.contrib.auth.forms import SetPasswordForm
from django.utils.translation import gettext_lazy as _

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
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'tag': forms.TextInput(attrs={'class': 'form-control'}),
            'warehouse': forms.Select(attrs={'class': 'form-control selectpicker'}),
        }

class CourierForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'phone', 'address']

# class CourierForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['name', 'username', 'phone', 'address']

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.role = 'courier'  # Set the role here
#         if commit:
#             user.save()
#         return user

class ChangePasswordForm(SetPasswordForm):
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
        'password_entirely_numeric': _("Your password can't be entirely numeric."),
        'password_too_short': _("This password is too short. It must contain at least %(min_length)d characters."),
        'password_too_common': _("This password is too common."),
        'password_similar_to_username': _("The password is too similar to the username."),
    }

    old_password = forms.CharField(
        label=_("Old Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-control'}),
    )
    new_password1 = forms.CharField(
        label=_("New Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("Confirm New Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].validators.append(self.validate_password)

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError(_("The old password is incorrect."))
        return old_password

    def validate_password(self, password):
        password_validation.validate_password(password, self.user)