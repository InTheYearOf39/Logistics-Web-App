from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


# class User(AbstractUser):
#     is_sender= models.BooleanField('Is sender', default=False)
#     is_receiver = models.BooleanField('Is receiver', default=False)
#     is_courrier = models.BooleanField('Is courrier', default=False)


class User(AbstractUser):
    ROLE_CHOICES = (
        ('courier', 'courier'),
        ('sender', 'sender'),
        ('recipient', 'recipient'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='sender', verbose_name='role')

class Package(models.Model):
    STATUS_CHOICES = (
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    )
    
    packageName = models.CharField(max_length=100)
    packageDescripton = models.TextField()
    recipientName = models.CharField(max_length=100)
    recipientAddress = models.CharField(max_length=200)
    sendersAddress = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    
    def __str__(self):
        return self.title