from django.conf import settings
import africastalking

def send_sms(recipients, message, sender):
    africastalking_username = settings.AFRICASTALKING_USERNAME
    africastalking_api_key = settings.AFRICASTALKING_API_KEY

    africastalking.initialize(africastalking_username, africastalking_api_key)
    sms = africastalking.SMS
    try:
        response = sms.send(message, recipients, sender)
        print(response)
    except Exception as e:
        print(f'Ooooops!!!, we have a problem: {e}')

send_sms(["+256754891512"], "Your package-PN9876 has arrived congs: OTP is - 98765! Thanks for choosing Pudonet", "LASTMILE-PUDONET")


