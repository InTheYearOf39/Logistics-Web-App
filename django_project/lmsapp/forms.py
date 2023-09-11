from django import forms
from django.contrib.auth.forms import UserCreationForm
from lmsapp.models import User, Package, DropPickZone, Warehouse
from django.contrib.auth import password_validation
from django.contrib.auth.forms import SetPasswordForm
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, RegexValidator, MinLengthValidator, MaxLengthValidator
import re



def validate_custom_password(password):

    if password.isdigit():
        raise ValidationError(_("Password cannot be entirely numeric."))

    if not re.search(r'[A-Z]', password):
        raise ValidationError(_("Password must contain at least one capital letter."))

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValidationError(_("Password must contain at least one special character."))



class LoginForm(forms.Form):
    username = forms.CharField(
        required = True,
        widget= forms.TextInput(
            attrs={
                "class": "form-control control-sm",
                "placeholder": "username",
                'id': 'username',
                'name': 'username'
            }
        )
    )
    password = forms.CharField(
        required = True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control control-sm",
                "placeholder": "password",
                'id': 'password',
                'name': 'password'
            }
        )
    )


class SignUpForm(UserCreationForm):

    name = forms.CharField(
        required = True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control control-sm",
                "placeholder": "Full Name",
                'id': 'name',
                'name': 'name'
            }
        )
    )

    username = forms.CharField(
        required = True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control control-sm",
                "placeholder": "Username",
                'id': 'username',
                'name': 'username'
            }
        )
    )

    email = forms.CharField(
    required = True,
    widget=forms.TextInput(
        attrs={
            "class": "form-control control-sm",
            "placeholder": "Email"
        }
    ),
    validators=[EmailValidator(message='Please enter a valid email address.')],
    )

    password1 = forms.CharField(
        required = True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control control-sm",
                "placeholder": "Password",
                'id': 'password1',
                'name': 'password1'

            }
        ),
        validators=[
            MinLengthValidator(8, message='Password must be at least 8 characters long'),
            MaxLengthValidator(100, message='Password cannot be more than 100 characters long'),
            validate_custom_password
        ]
    )

    password2 = forms.CharField(
        required = True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control control-sm",
                "placeholder": "Confirm Password",
                'id': 'password2',
                'name': 'password2'
            }
        ),
        validators=[
            MinLengthValidator(8, message='Password must be at least 8 characters long'),
            MaxLengthValidator(100, message='Password cannot be more than 100 characters long'),
            validate_custom_password
        ]
    )


    class Meta:
        model = User
        fields = ('name', 'username', 'email', 'password1', 'password2')


def validate_not_entirely_numeric(value):
    if value.isdigit():
        raise ValidationError("Package name cannot be entirely numeric.")
    

class PackageForm(forms.ModelForm):

    DELIVERY_TYPE_CHOICES = [
        ('', '-- Select Delivery Type --'),
        ('standard', 'Standard'),
        ('premium', 'Premium'),
        ('express', 'Express'),
    ]

    GENDER_TYPE_CHOICES = [
        ('', '-- Select Gender --' ),
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    packageName = forms.CharField(
        required = True,
        validators=[
            MinLengthValidator(3, message='Package name should have at least 3 characters.'),
            MaxLengthValidator(100, message='Package name cannot have more than 100 characters.'),
            RegexValidator(regex=re.compile(r'(.*[a-zA-Z0-9]){2,}'), message='Package name cannot be entirely special characters.'), 
            validate_not_entirely_numeric
        ],
        widget = forms.TextInput(attrs={'class': 'form-control form-control-sm', 'id': 'packageName', 'name': 'packageName', 'placeholder': 'Package Name'})
    )

    packageDescription = forms.CharField(
        required = True,
        validators=[
            MinLengthValidator(5, message='Package description should have at least 5 characters.'),
            MaxLengthValidator(500, message='Package description cannot have more than 100 characters.'),
            validate_not_entirely_numeric
        ],
        widget=forms.Textarea(attrs={'class': 'form-control form-control-sm', 'style': 'resize: vertical; height: 60px;', 'id': 'packageDescription', 'name': 'packageDescription', 'placeholder': 'Enter Description'}),
    )

    deliveryType = forms.ChoiceField(
        required = True,
        choices=DELIVERY_TYPE_CHOICES,
        widget = forms.Select(attrs={'class': 'form-select form-select-sm selectpicker', 'id': 'deliveryType', 'name': 'deliveryType' }),
    )

    dropOffLocation = forms.ModelChoiceField(
        required = False,
        queryset = DropPickZone.objects.all(),
        empty_label = "-- Select Drop Off Location --",
        widget = forms.Select(attrs={'class': 'form-control form-control-sm selectpicker', 'id': 'dropOffLocation', 'name': 'dropOffLocation'})
    )

    recipientName = forms.CharField(
        required = True,
        validators=[
            MinLengthValidator(3, message='recipient name should have at least 3 characters.'),
            MaxLengthValidator(100, message='recipient name cannot have more than 100 characters.')
        ],
        widget = forms.TextInput(attrs={'class': 'form-control form-control-sm', 'id': 'recipientName', 'name': 'recipientName', 'placeholder': 'Recipient Name'})
    )

    recipientEmail = forms.CharField(
        required = False,
        validators=[EmailValidator(message='Please enter a valid email address.')],
        widget = forms.TextInput(attrs={'class': 'form-control form-control-sm', 'id': 'recipientEmail', 'name': 'recipientEmail', 'placeholder': 'Recipient Email'})
    )

    recipientTelephone = forms.CharField(
        required = True,
        validators=[
            RegexValidator(
                regex=r'^0\d{9}$',
                message='Please enter a valid ten-digit telephone number'
            )
        ],
        widget = forms.TextInput(attrs={'class': 'form-control form-control-sm', 'id': 'recipientTelephone', 'name': 'recipientTelephone', 'placeholder': 'Recipient Telephone'})
    )

    recipientAddress = forms.CharField(
        required = True,
        validators=[
            MinLengthValidator(4, message='Recipient address should have at least 4 characters.'),
            MaxLengthValidator(200, message='Recipient address cannot have more than 200 characters.')
        ],
        widget = forms.TextInput(attrs={'class': 'form-control form-control-sm', 'id': 'recipientAddress', 'name': 'recipientAddress', 'placeholder': 'Recipient Address', 'onkeyup': 'calculateDeliveryFee()' })
    )

    recipientIdentification = forms.CharField(
        required = False,
        validators=[
            MinLengthValidator(5, message='Recipient identification should have at least 5 characters.'),
            MaxLengthValidator(50, message='Recipient identification cannot have more than 50 characters.')
        ],
        widget = forms.TextInput(attrs={'class': 'form-control form-control-sm', 'id': 'recipientIdentification', 'name': 'recipientIdentification', 'placeholder':'Enter Recipient ID' })
    )

    genderType = forms.ChoiceField(
        required = False,
        choices=GENDER_TYPE_CHOICES,
        widget = forms.Select(attrs={'class': 'form-control form-control-sm', 'id': 'genderType', 'name': 'genderType'})
    )

    sendersName = forms.CharField(
        required = False,
        validators=[
            MinLengthValidator(3, message='recipient name should have at least 3 characters.'),
            MaxLengthValidator(100, message='recipient name cannot have more than 100 characters.')
        ],
        widget = forms.TextInput(attrs={'class': 'form-control form-control-sm', 'id': 'sendersName', 'name': 'sendersName', 'placeholder': "Sender's Name" })
    )

    sendersEmail = forms.CharField(
        required = False,
        validators=[EmailValidator(message='Please enter a valid email address.')],
        widget = forms.TextInput(attrs={'class': 'form-control form-control-sm', 'id': 'senderEmail', 'name': 'senderEmail', 'placeholder': "Sender's Email"})
    )

    sendersContact = forms.CharField(
        required = True,
        validators=[
            RegexValidator(
                regex=r'^0\d{9}$',
                message='Please enter a valid ten-digit telephone number'
            )
        ],
        widget = forms.TextInput(attrs={'class': 'form-control form-control-sm', 'id': 'sendersContact', 'name': 'sendersContact', 'placeholder': 'Sender Contact'})
    )

    sendersAddress = forms.CharField(
        required = False,
        validators=[
            MinLengthValidator(4, message='sender address should have at least 4 characters.'),
            MaxLengthValidator(200, message='sender address cannot have more than 200 characters.')
        ],
        widget = forms.TextInput(attrs={'class': 'form-control form-control-sm', 'id': 'senderAddress', 'name': 'senderAddress', 'placeholder': "Sender's Address",'onkeyup': 'calculateDeliveryFee()'})
    )

    recipientPickUpLocation = forms.ModelChoiceField(
        required = False,
        queryset = DropPickZone.objects.all(),
        empty_label = "-- Select Recipient Pick-up Location --",
        widget = forms.Select(attrs={'class': 'form-control form-control-sm', 'id': 'recipientPickUpLocation', 'name': 'recipientPickUpLocation' })
    )

    deliveryFee = forms.CharField(
        required = False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'id': 'deliveryFeeInput', 'name': 'deliveryFee','placeholder': 'Delivery Fee', 'disabled': True })
    )


    def clean(self):
        cleaned_data = super().clean()
        delivery_type = cleaned_data.get('deliveryType')
        recipient_pick_up_location = cleaned_data.get('recipientPickUpLocation')
        # drop_off_location = cleaned_data.get('dropOffLocation')

        # if delivery_type == 'standard' and not drop_off_location:
        #     self.add_error('dropOffLocation', "Drop off location is required for standard delivery.")

        if delivery_type == 'standard' and not recipient_pick_up_location:
            self.add_error('recipientPickUpLocation', "Pick Up location is required for standard delivery.")

        return cleaned_data

    class Meta:
        model = Package
        fields = [
                  'packageName', 'deliveryType', 'dropOffLocation', 'packageDescription', 'recipientName', 
                  'recipientAddress', 'sendersAddress', 'recipientEmail', 'recipientTelephone', 'recipientPickUpLocation',
                  'recipientIdentification', 'genderType', 'sendersContact', 'deliveryFee', 'sendersName', 'sendersEmail', 
                  'warehouse', 'user',
                  ]
        widgets = {'warehouse': forms.TextInput(attrs={'class': 'form-control form-control-sm'})}


    
class WarehouseCreationForm(forms.ModelForm):
    
    name = forms.CharField(
            required = True,
            validators=[
            MinLengthValidator(4, message='Warehouse name should have at least 4 characters.'),
            MaxLengthValidator(40, message='Warehouse name cannot have more than 100 characters.'),
            RegexValidator(
                regex=r'^[A-Za-z\s\-]*$',
                message='Enter a valid name: Only letters, spaces, hyphens, and dashes are allowed.'
                ),
            ],
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'name': 'name', 'id': 'name', 'placeholder': 'Name'})
        )  

    address = forms.CharField(
        required = True,
        validators=[
        MinLengthValidator(3, message='Warehouse address should have at least 3 characters.'),
        MaxLengthValidator(200, message='Warehouse address cannot have more than 200 characters.')
            ],
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'id': 'address', 'name': 'address', 'placeholder': 'Address'})
        ) 

    phone = forms.CharField(
        required = True,
        validators=[
        RegexValidator(
        regex=r'^0\d{9}$',
        message='Please enter a valid ten-digit telephone number'
        )],
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'name': 'phone', 'placeholder': 'Phone number' })
        )

    tag = forms.CharField(
        required = True,
        validators=[
        RegexValidator(
        regex=r'^[A-Za-z\s\-]*$',
        message='Tag should only contain letters, hyphens, and underscores.',
        ),
        MinLengthValidator(3, message='Warehouse tag should have at least 3 characters.'),
        MaxLengthValidator(10, message='Warehouse tag cannot have more than 10 characters.')
            ],
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'name': 'tag', 'placeholder': 'Tag alias'})
        )

    class Meta:
        model = Warehouse
        fields = ['name', 'phone', 'address', 'tag']
        
    
class DropPickCreationForm(forms.ModelForm):
    
    name = forms.CharField(
            required = True,
            validators=[
            MinLengthValidator(4, message='Drop-Pick name should have at least 4 characters.'),
            MaxLengthValidator(40, message='Drop-Pick name cannot have more than 100 characters.'),
            RegexValidator(
                regex=r'^[A-Za-z\s\-]*$',
                message='Enter a valid name: Only letters, spaces, hyphens, and dashes are allowed.'
                ),
            ],
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'name': 'name', 'id': 'name', 'placeholder': 'Name'})
        )  

    address = forms.CharField(
        required = True,
        validators=[
        MinLengthValidator(3, message='Drop-Pick address should have at least 3 characters.'),
        MaxLengthValidator(200, message='Drop-Pick address cannot have more than 200 characters.')
            ],
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'id': 'address', 'name': 'address', 'placeholder': 'Address'})
        ) 
    
    warehouse = forms.ModelChoiceField(
        queryset=Warehouse.objects.all(),
        empty_label="Please select warehouse",
        widget=forms.Select(attrs={'class': 'form-control form-control-sm selectpicker'})
    )

    phone = forms.CharField(
        required = True,
        validators=[
        RegexValidator(
        regex=r'^0\d{9}$',
        message='Please enter a valid ten-digit telephone number'
        )],
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'name': 'phone', 'placeholder': 'Phone number' })
        )

    tag = forms.CharField(
        required = True,
        validators=[
        RegexValidator(
        regex=r'^[A-Za-z\s\-]*$',
        message='Tag should only contain letters, hyphens, and underscores.',
        ),
        MinLengthValidator(3, message='Drop-Pick tag should have at least 3 characters.'),
        MaxLengthValidator(10, message='Drop-Pick tag cannot have more than 10 characters.')
            ],
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'name': 'tag', 'placeholder': 'Tag alias'})
        )


    class Meta:
        model = DropPickZone
        fields = ['name', 'phone', 'address', 'tag', 'warehouse']

class WarehouseUserForm(forms.ModelForm):
    name = forms.CharField(
            required = True,
            validators = [
            MinLengthValidator(3, message='Warehouse admin name should have at least 3 characters.'),
            MaxLengthValidator(40, message='Warehouse admin name cannot have more than 100 characters.'),
            RegexValidator(
                regex=r'^[A-Za-z\s]*$',
                message='Enter a valid name: Only letters and spaces are allowed.'
                ),
            ],
        widget = forms.TextInput(attrs={'class': 'form-control form-control-sm', 'name': 'name', 'id': 'name', 'placeholder': 'Name'})
        )
    
    username = forms.CharField(
            required = True,
            validators = [
            MinLengthValidator(4, message='Warehouse admin username should have at least 4 characters.'),
            MaxLengthValidator(40, message='Warehouse admin username cannot have more than 100 characters.'),
            RegexValidator(
                regex = r'^[A-Za-z\s\-]*$',
                message ='Enter a valid username: Only letters, spaces, hyphens, and dashes are allowed.'
                ),
            ],
        widget = forms.TextInput(attrs={'class': 'form-control form-control-sm', 'name': 'username', 'id': 'username', 'placeholder': 'Username'})
        )  

    email = forms.CharField(
        validators=[EmailValidator(message='Please enter a valid email address.')],
        widget = forms.EmailInput(attrs={'class': 'form-control form-control-sm', 'name': 'email', 'id': 'email', 'placeholder': 'Email'})
    ) 
    
    warehouse = forms.ModelChoiceField(
        queryset = Warehouse.objects.all(),
        empty_label = "Please select Warehouse",
        widget = forms.Select(attrs={'class': 'form-control form-control-sm selectpicker'})
    )

    phone = forms.CharField(
        required = True,
        validators = [
        RegexValidator(
        regex = r'^0\d{9}$',
        message = 'Please enter a valid ten-digit telephone number'
        )],
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'name': 'phone', 'placeholder': 'Phone number' })
        )
 
    class Meta:
        model = User
        fields = ['name', 'username', 'phone', 'email', 'warehouse']

class DropPickUserForm(forms.ModelForm):
    name = forms.CharField(
            required = True,
            validators = [
            MinLengthValidator(3, message='Drop-Pick admin name should have at least 3 characters.'),
            MaxLengthValidator(40, message='Drop-Pick admin name cannot have more than 100 characters.'),
            RegexValidator(
                regex=r'^[A-Za-z\s]*$',
                message='Enter a valid name: Only letters and spaces are allowed.'
                ),
            ],
        widget = forms.TextInput(attrs={'class': 'form-control form-control-sm', 'name': 'name', 'id': 'name', 'placeholder': 'Name'})
        )
    
    username = forms.CharField(
            required = True,
            validators = [
            MinLengthValidator(4, message='Drop-Pick admin username should have at least 4 characters.'),
            MaxLengthValidator(40, message='Drop-Pick admin username cannot have more than 100 characters.'),
            RegexValidator(
                regex = r'^[A-Za-z\s\-]*$',
                message ='Enter a valid username: Only letters, spaces, hyphens, and dashes are allowed.'
                ),
            ],
        widget = forms.TextInput(attrs={'class': 'form-control form-control-sm', 'name': 'username', 'id': 'username', 'placeholder': 'Username'})
        )  

    email = forms.CharField(
        validators=[EmailValidator(message='Please enter a valid email address.')],
        widget = forms.EmailInput(attrs={'class': 'form-control form-control-sm', 'name': 'email', 'id': 'email', 'placeholder': 'Email'})
    ) 
    
    drop_pick_zone = forms.ModelChoiceField(
        queryset = DropPickZone.objects.all(),
        empty_label = "Please select drop pick zone",
        widget = forms.Select(attrs={'class': 'form-control form-control-sm selectpicker'})
    )

    phone = forms.CharField(
        required = True,
        validators = [
        RegexValidator(
        regex = r'^0\d{9}$',
        message = 'Please enter a valid ten-digit telephone number'
        )],
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'name': 'phone', 'placeholder': 'Phone number' })
        )
 
    class Meta:
        model = User
        fields = ['name', 'username', 'phone', 'email', 'drop_pick_zone']

class CourierForm(forms.ModelForm):
    name = forms.CharField(
            required = True,
            validators = [
            MinLengthValidator(3, message="Courier's name should have at least 3 characters."),
            MaxLengthValidator(40, message="Courier's name cannot have more than 100 characters."),
            RegexValidator(
                regex=r'^[A-Za-z\s]*$',
                message='Enter a valid name: Only letters and spaces are allowed.'
                ),
            ],
        widget = forms.TextInput(attrs={'class': 'form-control form-control-sm', 'name': 'name', 'id': 'name', 'placeholder': 'Name'})
        )
    
    username = forms.CharField(
            required = True,
            validators = [
            MinLengthValidator(4, message="Courier's username should have at least 4 characters."),
            MaxLengthValidator(40, message="Courier's username cannot have more than 100 characters."),
            RegexValidator(
                regex = r'^[A-Za-z\s\-]*$',
                message ='Enter a valid username: Only letters, spaces, hyphens, and dashes are allowed.'
                ),
            ],
        widget = forms.TextInput(attrs={'class': 'form-control form-control-sm', 'name': 'username', 'id': 'username', 'placeholder': 'Username'})
        )  

    email = forms.CharField(
        validators=[EmailValidator(message='Please enter a valid email address.')],
        widget = forms.EmailInput(attrs={'class': 'form-control form-control-sm', 'name': 'email', 'id': 'email', 'placeholder': 'Email'})
    )

    phone = forms.CharField(
        required = True,
        validators = [
        RegexValidator(
            regex = r'^0\d{9}$',
            message = 'Please enter a valid ten-digit telephone number'
            )],
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'name': 'phone', 'id': 'phone', 'placeholder': 'Phone number' })
        )
    
    address = forms.CharField(
        required = True,
        validators=[
        MinLengthValidator(3, message='Address should have at least 3 characters.'),
        MaxLengthValidator(200, message='Address cannot have more than 200 characters.')
            ],
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'id': 'address', 'name': 'address', 'placeholder': 'Address'})
        ) 
    
    warehouse = forms.ModelChoiceField(
        required = True,
        queryset = Warehouse.objects.all(),
        empty_label = "Please select a warehouse",
        widget = forms.Select(attrs={'class': 'form-control form-control-sm selectpicker'})
    )

    class Meta:
        model = User
        fields = ['name', 'username', 'phone', 'address', 'warehouse', 'email']


class EditWarehouseUserForm(forms.ModelForm):
    name = forms.CharField(
        widget = forms.TextInput(attrs={'class': 'form-control form-control-sm bg-light', 'name': 'name', 'id': 'name', 'placeholder': 'Name', 'readonly': True })
        )
    
    username = forms.CharField(
        widget = forms.TextInput(attrs={'class': 'form-control form-control-sm bg-light', 'name': 'username', 'id': 'username', 'placeholder': 'Username', 'readonly': True })
        )  

    email = forms.CharField(
        widget = forms.EmailInput(attrs={'class': 'form-control form-control-sm bg-light', 'name': 'email', 'id': 'email', 'placeholder': 'Email', 'readonly': True })
    ) 

    warehouse = forms.ModelChoiceField(
        required = True,
        queryset = Warehouse.objects.all(),
        empty_label = "Please select Warehouse",
        widget = forms.Select(attrs={'class': 'form-control form-control-sm selectpicker'})
    )

    phone = forms.CharField(
        required = True,
        validators = [
        RegexValidator(
        regex = r'^0\d{9}$',
        message = 'Please enter a valid ten-digit telephone number'
        )],
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'name': 'phone', 'placeholder': 'Phone number' })
        )
 
    class Meta:
        model = User
        fields = ['phone',  'warehouse', 'email', 'username', 'name']

class EditDropPickUserForm(forms.ModelForm):
    name = forms.CharField(
        widget = forms.TextInput(attrs={'class': 'form-control form-control-sm bg-light', 'name': 'name', 'id': 'name', 'placeholder': 'Name', 'readonly': True })
        )
    
    username = forms.CharField(
        widget = forms.TextInput(attrs={'class': 'form-control form-control-sm bg-light', 'name': 'username', 'id': 'username', 'placeholder': 'Username', 'readonly': True })
        )  

    email = forms.CharField(
        widget = forms.EmailInput(attrs={'class': 'form-control form-control-sm bg-light', 'name': 'email', 'id': 'email', 'placeholder': 'Email', 'readonly': True })
    ) 

    drop_pick_zone = forms.ModelChoiceField(
        required = True,
        queryset = DropPickZone.objects.all(),
        empty_label = "Please select a drop pick zone",
        widget = forms.Select(attrs={'class': 'form-control form-control-sm selectpicker'})
    )

    phone = forms.CharField(
        required = True,
        validators = [
        RegexValidator(
        regex = r'^0\d{9}$',
        message = 'Please enter a valid ten-digit telephone number'
        )],
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'name': 'phone', 'placeholder': 'Phone number' })
        )
    
    
    class Meta:
        model = User
        fields = ['phone',  'drop_pick_zone', 'email', 'username', 'name']


class EditCourierForm(forms.ModelForm):
    name = forms.CharField(
        widget = forms.TextInput(attrs={'class': 'form-control form-control-sm bg-light', 'name': 'name', 'id': 'name', 'placeholder': 'Name', 'readonly': True })
        )
    
    username = forms.CharField(
        widget = forms.TextInput(attrs={'class': 'form-control form-control-sm bg-light', 'name': 'username', 'id': 'username', 'placeholder': 'Username', 'readonly': True })
        )  

    email = forms.CharField(
        widget = forms.EmailInput(attrs={'class': 'form-control form-control-sm bg-light', 'name': 'email', 'id': 'email', 'placeholder': 'Email', 'readonly': True })
    ) 

    phone = forms.CharField(
        required = True,
        validators = [
        RegexValidator(
            regex = r'^0\d{9}$',
            message = 'Please enter a valid ten-digit telephone number'
            )],
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'name': 'phone', 'id': 'phone', 'placeholder': 'Phone number' })
        )
    
    address = forms.CharField(
        required = True,
        validators=[
        MinLengthValidator(3, message='Address should have at least 3 characters.'),
        MaxLengthValidator(200, message='Address cannot have more than 200 characters.')
            ],
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'id': 'address', 'name': 'address', 'placeholder': 'Address'})
        ) 
    
    warehouse = forms.ModelChoiceField(
        required = True,
        queryset = Warehouse.objects.all(),
        empty_label = "Please select a warehouse",
        widget = forms.Select(attrs={'class': 'form-control form-control-sm selectpicker'})
    )

    class Meta:
        model = User
        fields = ['name', 'username', 'phone', 'address', 'warehouse', 'email']


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