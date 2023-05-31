# decorators.py
from django.shortcuts import redirect

def recipient_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_recipient:
            return redirect('login')  # Redirect to login page if not authenticated or not a recipient
        return view_func(request, *args, **kwargs)
    return wrapper
