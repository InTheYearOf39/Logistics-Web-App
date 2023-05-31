# custom_backend.py
from django.contrib.auth.backends import ModelBackend
from .models import User

class CustomBackend(ModelBackend):
   def user_can_authenticate(self, user):
        if isinstance(user, User):
            return user.is_active and user.is_recipient
        return False
