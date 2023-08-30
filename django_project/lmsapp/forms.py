from django import forms
from django.contrib.auth.forms import UserCreationForm
from lmsapp.models import User, Package, DropPickZone
from django.contrib.auth import password_validation
from django.contrib.auth.forms import SetPasswordForm
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, RegexValidator, MinLengthValidator, MaxLengthValidator

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
        fields = ('name', 'username', 'email', 'password1', 'password2', 'tag')


class PackageForm(forms.ModelForm):

    class Meta:
        model = Package
        fields = ['packageName', 'deliveryType', 'dropOffLocation', 'packageDescription', 'recipientName', 'recipientAddress', 'sendersAddress', 'recipientEmail', 'recipientTelephone', 'recipientPickUpLocation', 'recipientIdentification', 'genderType', 'sendersContact', 'deliveryFee', 'sendersName', 'sendersEmail', 'warehouse', 'user']
        widgets = {
            'packageName': forms.TextInput(attrs={'class': 'form-control'}),
            'deliveryType': forms.TextInput(attrs={'class': 'form-control'}),
            'dropOffLocation': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'recipientPickUpLocation': forms.TextInput(attrs={'class': 'form-control'}),
            'packageDescription': forms.TextInput(attrs={'class': 'form-control'}),
            'recipientName': forms.TextInput(attrs={'class': 'form-control'}),
            'recipientEmail': forms.TextInput(attrs={'class': 'form-control'}),
            'recipientTelephone': forms.TextInput(attrs={'class': 'form-control'}),
            'recipientAddress': forms.TextInput(attrs={'class': 'form-control'}),
            'recipientIdentification': forms.TextInput(attrs={'class': 'form-control'}),
            'deliveryFee': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'genderType': forms.TextInput(attrs={'class': 'form-control'}),
            'sendersName': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'sendersEmail': forms.TextInput(attrs={'class': 'form-control'}),
            'sendersAddress': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'sendersContact': forms.TextInput(attrs={'class': 'form-control'}),
            'warehouse': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
        }

    packageName = forms.CharField(
        required = True,
        validators=[
            MinLengthValidator(3, message='Package name should have at least 3 characters.'),
            MaxLengthValidator(100, message='Package name should have at most 100 characters.')
        ]
    )

    packageDescription = forms.CharField(
        required = True,
        validators=[
            MinLengthValidator(3, message='Package description should have at least 3 characters.'),
            MaxLengthValidator(500, message='Package description should have at most 100 characters.')
        ]
    )

    deliveryType = forms.ChoiceField(
        required = True,
        choices=Package.DELIVERY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    recipientPickUpLocation = forms.ModelChoiceField(
        queryset=DropPickZone.objects.all(),
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    recipientName = forms.CharField(
        required = True,
        validators=[
            MinLengthValidator(3, message='recipient name should have at least 3 characters.'),
            MaxLengthValidator(100, message='recipient name should have at most 100 characters.')
        ]
    )

    recipientEmail = forms.CharField(
        validators=[EmailValidator(message='Please enter a valid email address.')]
    )

    recipientTelephone = forms.CharField(
        required = True,
        validators=[
            RegexValidator(
                regex=r'^\+?\d{9,15}$',
                message='Please enter a valid phone number.'
            )
        ]
    )

    recipientAddress = forms.CharField(
        validators=[
            MinLengthValidator(10, message='Recipient address should have at least 10 characters.'),
            MaxLengthValidator(200, message='Recipient address should have at most 200 characters.')
        ]
    )

    recipientIdentification = forms.CharField(
        validators=[
            MinLengthValidator(5, message='Recipient identification should have at least 5 characters.'),
            MaxLengthValidator(50, message='Recipient identification should have at most 50 characters.')
        ]
    )

    genderType = forms.ChoiceField(
        required = True,
        choices=Package.DELIVERY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    sendersName = forms.CharField(
        required = True,
        validators=[
            MinLengthValidator(3, message='recipient name should have at least 3 characters.'),
            MaxLengthValidator(100, message='recipient name should have at most 100 characters.')
        ]
    )

    sendersEmail = forms.CharField(
        validators=[EmailValidator(message='Please enter a valid email address.')]
    )

    sendersContact = forms.CharField(
        required = True,
        validators=[
            RegexValidator(
                regex=r'^\+?\d{9,15}$',
                message='Please enter a valid phone number.'
            )
        ]
    )

    sendersAddress = forms.CharField(
        validators=[
            MinLengthValidator(10, message='sender address should have at least 10 characters.'),
            MaxLengthValidator(200, message='sender address should have at most 200 characters.')
        ]
    )

    
class WarehouseForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'phone', 'address', 'tag', 'email']

class DropPickForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'phone', 'email', 'address', 'tag', 'warehouse']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'tag': forms.TextInput(attrs={'class': 'form-control'}),
            'warehouse': forms.Select(attrs={'class': 'form-control selectpicker'}),
        }

class CourierForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'phone', 'address', 'warehouse', 'email']

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


class ApiForm(forms.Form):
    password = forms.CharField(
        max_length=150,
        label="Enter Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-sm",
                "placeholder": "Enter password",
                "type": "password",
                "name": "generateApiKey",
                "id": "generateApiKey"
            }
        )
    )

class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField(
        label="Upload Excel File",
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file btn btn-secondary'})
    )