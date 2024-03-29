from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils import timezone
import random
import string
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string

class CustomUserManager(UserManager):
    def create_admin(self, username, password):
        admin = self.create_user(username=username, password=password)
        admin.is_staff = True
        admin.is_superuser = True
        admin.role = 'admin'
        admin.save()
        return admin


class Warehouse(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    tag = models.CharField(max_length=10, null=True, blank=True)
    latitude = models.FloatField( null=True, blank=True)
    longitude = models.FloatField( null=True, blank=True)
    
    created_on = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL
                                   , related_name='warehouse_created_by', null=True)
    modified_on = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL
                                   , related_name='warehouse_modified_by', null=True)
    

    def save(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        if not self.pk:
            self.created_by = user
            super(Warehouse, self).save(*args, **kwargs)
        else:
            self.modified_by = user
            super(Warehouse, self).save(*args, **kwargs)
    
    def __str__(self):
        return str(self.name)

class DropPickZone(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name='drop_pick_zones')
    tag = models.CharField(max_length=10, null=True, blank=True)
    latitude = models.FloatField( null=True, blank=True)
    longitude = models.FloatField( null=True, blank=True)
    
    created_on = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL
                                   , related_name='drop_pick_zones_created_by', null=True)
    modified_on = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL
                                   , related_name='drop_pick_zones_modified_by', null=True)
    
    def save(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        if not self.pk:
            self.created_by = user
            super(DropPickZone, self).save(*args, **kwargs)
        else:
            self.modified_by = user
            super(DropPickZone, self).save(*args, **kwargs)
 

    def __str__(self):
        return str(self.name)


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('courier', 'Courier'),
        ('sender', 'Sender'),
        ('drop_pick_zone', 'Drop/Pick Zone'),
        ('warehouse', 'Warehouse'),
    )
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('on-trip', 'On Trip'),
    )
    name = models.CharField(max_length=40, null=False)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, verbose_name='Role', null=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    objects = CustomUserManager()
    verification_token = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True )
    has_set_password = models.BooleanField(default=False)

    # Add warehouse-specific fields
    phone = models.CharField(max_length=20, null=True, blank=True)
    drop_pick_zone = models.ForeignKey(DropPickZone, related_name='users', on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)

    # Add drop_pick_zone-specific fields
    warehouse = models.ForeignKey(Warehouse, related_name='users', on_delete=models.SET_NULL, null=True, blank=True)


    created_on = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey('self', on_delete=models.SET_NULL,
                                   related_name='user_created_by', null=True)
    modified_on = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey('self', on_delete=models.SET_NULL,
                                    related_name='user_modified_by', null=True)
    
    
    def generate_verification_token(self, length=64):
        token = get_random_string(length)
        self.verification_token = token
        return token
    
    def save(self, *args, **kwargs):
        # if not self.pk:
        #     self.generate_verification_token()
        return super().save(*args, **kwargs)

    def __str__(self):
        return str(self.username)
    


class Package(models.Model):
    STATUS_CHOICES = (
        ('upcoming', 'Upcoming'),
        ('dropped_off', 'Dropped Off'),
        ('dispatched', 'Dispatched'),
        ('en_route', 'En Route'),
        ('warehouse_arrival', 'Warehouse Arrival'),
        ('in_house', 'In House'),
        ('in_transit', 'In Transit'),
        ('at_pickup', 'At Pickup'),
        ('ready_for_pickup', 'Ready for Pickup'),
        ('arrived', 'Arrived'),
        ('completed', 'Completed'),
    )

    DELIVERY_CHOICES = (
        ('standard', 'Standard'),
        ('premium', 'Premium'),
        ('express', 'Express'),
    )
    
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )

    PACKAGE_PREFIX = 'pn'

    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='packages', null=True, blank=True)
    courier = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='assigned_packages', null=True, blank=True)
    packageName = models.CharField(max_length=100, null=True, blank=True)
    deliveryType = models.CharField(max_length=20, choices=DELIVERY_CHOICES, null=True, blank=True)
    dropOffLocation = models.ForeignKey(DropPickZone, on_delete=models.SET_NULL, null=True, blank=True, default=None, related_name='dropped_off_at')
    recipientPickUpLocation = models.ForeignKey(DropPickZone, on_delete=models.SET_NULL, null=True, blank=True, default=None, related_name='packages_picked_up')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, null=True, blank=True, related_name='packages_in_house')
    packageDescription = models.TextField(max_length=500, null=True, blank=True)
    recipientName = models.CharField(max_length=100, null=True, blank=True)
    recipientEmail = models.CharField(max_length=100, null=True, blank=True)
    recipientTelephone = models.CharField(max_length=100, null=True, blank=True)
    recipientAddress = models.CharField(max_length=200, null=True, blank=True)
    recipientIdentification = models.CharField(max_length=200, null=True, blank=True)
    sendersName = models.CharField(max_length=200, null=True, blank=True)
    sendersEmail = models.CharField(max_length=200, null=True, blank=True)
    sendersAddress = models.CharField(max_length=200, null=True, blank=True)
    sendersContact = models.CharField(max_length=200, null=True, blank=True)
    sender_latitude = models.FloatField( null=True, blank=True)
    sender_longitude = models.FloatField( null=True, blank=True)
    recipient_latitude = models.FloatField( null=True, blank=True)
    recipient_longitude = models.FloatField( null=True, blank=True)
    deliveryFee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    genderType = models.CharField(max_length=20, choices=GENDER_CHOICES, verbose_name='Gender', null=True, blank=True)
    package_number = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')  # default status is 'upcoming'
    
    created_on = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='packages_created_by', null=True)
    modified_on = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='packages_modified_by', null=True)
    
    received_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    in_house_at = models.DateTimeField(null=True, blank=True)
    dispatched_at = models.DateTimeField(null=True, blank=True)
    assigned_at = models.DateTimeField(default=timezone.now)
    otp = models.CharField(max_length=6, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.package_number:
            self.package_number = self.generate_package_number()

        if self.status in ['dropped_off', 'in_house', 'ready_for_pickup']:
            if self.status == 'dropped_off':
                self.package_number = f"{self.dropOffLocation.tag}-{self.package_number}"
            
            if self.status == 'in_house' and self.warehouse:
                self.package_number = f"{self.warehouse.tag}-{self.package_number}"
                                
            if self.status == 'ready_for_pickup':
                self.package_number = f"{self.dropOffLocation.tag}-{self.package_number}"
                
        super().save(*args, **kwargs)

        if self.courier:
            CourierHistory.objects.create(
                courier=self.courier,
                status=self.status,
                package=self,
                timestamp=self.modified_on
            )

    def generate_package_number(self):
        package_number = Package.PACKAGE_PREFIX + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        return package_number

    def clean(self):
        if self.dropOffLocation and self.warehouse:
            raise ValidationError("A package cannot have both drop-off location and warehouse assigned.")

    def __str__(self):
        return str(self.packageName)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)


class APIKey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    api_key = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"API Key for {str(self.user.username)}"


class UserGoogleSheet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    google_sheet_url = models.URLField(blank=True, null=True, unique=True)
    header_mapping = models.JSONField(default=dict)

    def __str__(self):
        return f"Google sheet: {str(self.user.username)}"
    

class CourierLocationData(models.Model):
    courier = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    latitude = models.FloatField( null=True, blank=True)
    longitude = models.FloatField( null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Selected courier: {str(self.courier.username)}"

class CourierHistory(models.Model):
    courier = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=Package.STATUS_CHOICES)
    package = models.ForeignKey(Package, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
   