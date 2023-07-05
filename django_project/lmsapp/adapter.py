from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model

User = get_user_model()

#Creates a new user instance based on the information provided by the social account; this instance is created with the user role, 'sender'.
class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form=form)

        user.role = 'sender'
        user.save()

        return user
