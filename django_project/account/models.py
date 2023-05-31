from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    is_sender= models.BooleanField('Is sender', default=False)
    is_receiver = models.BooleanField('Is receiver', default=False)
    is_courrier = models.BooleanField('Is courrier', default=False)