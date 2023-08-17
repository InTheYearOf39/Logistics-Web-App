from django.shortcuts import render, redirect, redirect
from django.contrib.auth import authenticate, login, logout
from lmsapp.forms import SignUpForm, LoginForm
from lmsapp.models import User
from django.contrib import messages
from lmsapp.forms import ChangePasswordForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.conf import settings
from lmsapp.utils import generate_and_store_api_key
from lmsapp.forms import ApiForm


"""
A function to handle user registration. The form data is validated, and if valid, a user is created, saved to the database, 
and An email is sent to the user with a verification token. The user is then redirected to the email_verification_sent template.
If the form is not valid or the request method is not POST, the registration form is displayed.
"""
def register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'sender'
            user.is_active = False  

            user.generate_verification_token()
            user.save()
            # Send verification email
            current_site = get_current_site(request)
            subject = 'Activate your account'
            message = f"A new account matching this email was detected on our system,\n"\
                      f"Click the following link to activate your account:\n\n" \
                      f"{current_site.domain}/verify-email?verification_token={user.verification_token}\n"\
                      f"If this wasn't you, ignore this message"
            
            send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])
            
            msg = 'user created'
            return redirect('email_verification_sent')
        else:
            msg = 'form is not valid'
    else:
        form = SignUpForm()
    return render(request, 'auth/register.html', {'form': form, 'msg': msg})

def verify_email(request):
    token = request.GET.get('verification_token')
    user = User.objects.get(verification_token=token)
    
    if user:
        user.is_active = True
        user.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        return redirect('sender_dashboard')
    else:
        return redirect('email_verification_failed')

"""
A function to handle user login. The form data is validated, and if valid, the user is authenticated and logged in. 
The user is then redirected to their respective dashboard based on their role. If the form is not valid or the request method is not POST, the login form is displayed.
 """
def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                dashboard_mapping = {
                        'admin': 'admin_dashboard',
                        'courier': 'courier_dashboard',
                        'sender': 'sender_dashboard',
                        'drop_pick_zone': 'drop_pick_zone_dashboard',
                        'warehouse': 'warehouse_dashboard',
                    }
                dashboard_url = dashboard_mapping.get(user.role)
                if dashboard_url:
                    return redirect(dashboard_url)
            else:
                msg= 'invalid credentials'
        else:
            msg = 'error validating form'
    return render(request, 'auth/login.html', {'form': form, 'msg': msg})

""""A function to notify a user when an account verification token has been sent"""
def email_verification_sent(request):
    return render(request, 'auth/email_verification_sent.html')

""""A function to notify a user when their account verification has failed"""
def email_verification_failed(request):
    return render(request, 'auth/email_verification_failed.html')

"""
A function to handle user logout. When a user accesses this view, they will be logged out 
and redirected to the 'index.html/' template.
"""
def logout_user(request):
    logout(request)
    return redirect('index.html/')

"""
A function to handle password change for a user. The form data is validated, and if valid, 
the user's password is updated and the session authentication hash is updated. The user is 
then redirected to their respective dashboard based on their role. If the form is not valid 
or the request method is not POST, the password change form is displayed.
"""
def change_password(request):
    # Mapping of user roles to dashboard URLs
    dashboard_urls = {
        'warehouse': 'warehouse_dashboard',
        'admin': 'admin_dashboard',
        'courier': 'courier_dashboard',
        'sender': 'sender_dashboard',
        'drop_pick_zone': 'drop_pick_zone_dashboard',
    }
    
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to update the session
            messages.success(request, 'Your password has been successfully changed.')
            
            # Redirect to the user type dashboard based on the user's role
            user_role = user.role
            if user_role in dashboard_urls:
                dashboard_url = dashboard_urls[user_role]
                return redirect(dashboard_url)
            else:
                # Handle the case when the user's role is not in the mapping object
                return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = ChangePasswordForm(request.user)
    return render(request, 'change_password.html', {'form': form})

def generate_api_key(request):
    if request.method == 'POST':
        form = ApiForm(request.POST)
        user = request.user
        username = user.username

        if form.is_valid():            
            password = form.cleaned_data['password']
            
            try:
                # user = User.objects.get(username=username)
                user = authenticate(username=username, password=password)
                if user:
                    api_key = generate_and_store_api_key(user)
                    return render(request, 'api_key_generated.html', {'api_key': api_key})
                else:
                    error_message = "Wrong Credentials!!!!."
            except User.DoesNotExist:
                error_message = "User does not exist."
        else:
            error_message = "Invalid form data."

        return render(request, 'auth/generate_api_key.html', {'form': form, 'error_message': error_message})
    else:
        form = ApiForm()

    return render(request, 'auth/generate_api_key.html', {'form': form})