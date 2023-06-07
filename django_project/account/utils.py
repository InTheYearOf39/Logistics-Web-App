import datetime
import secrets

def get_time_of_day():
    current_hour = datetime.datetime.now().hour

    if 5 <= current_hour < 12:
        return "Good Morning"
    elif 12 <= current_hour < 18:
        return "Good Afternoon"
    else:
        return "Good Evening"


def generate_one_time_pin():
    pin_length = 6  
    
    characters = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    one_time_pin = ''.join(secrets.choice(characters) for _ in range(pin_length))
    
    return one_time_pin
