from lmsapp.models import APIKey
from django.conf import settings
import africastalking
import random
import string


def send_sms(recipients, message, sender):
    africastalking_username = settings.AFRICASTALKING_USERNAME
    africastalking_api_key = settings.AFRICASTALKING_API_KEY

    africastalking.initialize(africastalking_username, africastalking_api_key)
    sms = africastalking.SMS
   
    try:
        response = sms.send(message, recipients, sender)
    except Exception as e:
        print(f'Ooooops!!!, we have a problem: {e}')


def generate_api_key(length=48):
    characters = string.ascii_letters + string.digits
    api_key = ''.join(random.choice(characters) for _ in range(length))
    return api_key

def generate_and_store_api_key(user, length=48):
    existing_api_key = APIKey.objects.filter(user=user).first()

    if existing_api_key:
        return existing_api_key.api_key

    api_key = generate_api_key(length)

    api_key_obj = APIKey(user=user, api_key=api_key)
    api_key_obj.save()

    return api_key
