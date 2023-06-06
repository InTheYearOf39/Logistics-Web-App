from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import random
import string

# Create your models here.

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'admin'),
        ('courier', 'courier'),
        ('sender', 'sender'),
        ('recipient', 'recipient'),
    )
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('on-trip', 'On Trip'),
    )
    name = models.CharField(max_length=20, null=False)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, verbose_name='role', null=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')

    def __str__(self):
        return self.username
        
# class User(AbstractUser):
#     ROLE_CHOICES = (
#         ('admin', 'admin'),
#         ('courier', 'courier'),
#         ('sender', 'sender'),
#         ('recipient', 'recipient'),
#     )
#     name = models.CharField(max_length=20,null=False)
#     role = models.CharField(max_length=10, choices=ROLE_CHOICES, verbose_name='role', null=False)

class Package(models.Model):
    STATUS_CHOICES = (
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    )

    PACKAGE_PREFIX = 'dn'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='packages', null=True)
    courier = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='assigned_packages', null=True, blank=True)
    packageName = models.CharField(max_length=100)
    packageDescription = models.TextField()
    recipientName = models.CharField(max_length=100)
    recipientAddress = models.CharField(max_length=200)
    sendersAddress = models.CharField(max_length=200)
    delivery_number = models.CharField(max_length=7, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.packageName

    def save(self, *args, **kwargs):
        if self.courier is None and self.status == 'ongoing':
            raise ValueError("Courier must be assigned for packages with 'ongoing' status.")
        if not self.delivery_number:
            self.delivery_number = self._generate_delivery_number()
        super().save(*args, **kwargs)

    def _generate_delivery_number(self):
        digits = ''.join(random.choices(string.digits, k=5))
        return f'{self.PACKAGE_PREFIX}{digits}'

# class Package(models.Model):
#     STATUS_CHOICES = (
#         ('upcoming', 'Upcoming'),
#         ('ongoing', 'Ongoing'),
#         ('completed', 'Completed'),
#     )

#     PACKAGE_PREFIX = 'dn'
    
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='packages', null=True)
#     packageName = models.CharField(max_length=100)
#     packageDescription = models.TextField()
#     recipientName = models.CharField(max_length=100)
#     recipientAddress = models.CharField(max_length=200)
#     sendersAddress = models.CharField(max_length=200)
#     delivery_number = models.CharField(max_length=7, unique=True)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    
#     def __str__(self):
#         return self.packageName
    
#     def save(self, *args, **kwargs):
#         if not self.delivery_number:
#             self.delivery_number = self._generate_delivery_number()
#         super().save(*args, **kwargs)

#     def _generate_delivery_number(self):
#         digits = ''.join(random.choices(string.digits, k=5))
#         return f'{self.PACKAGE_PREFIX}{digits}'