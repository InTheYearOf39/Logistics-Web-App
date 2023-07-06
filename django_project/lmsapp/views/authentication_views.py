from django.shortcuts import render, redirect, redirect
from django.contrib.auth import authenticate, login, logout
from lmsapp.forms import SignUpForm, LoginForm
from django.contrib import messages
from lmsapp.forms import ChangePasswordForm
from django.contrib.auth import update_session_auth_hash


"""
A function to handle user registration. The form data is validated, and if valid, a user is created, saved to the database, and logged in. The user is then redirected to their respective dashboard based on their role.
If the form is not valid or the request method is not POST, the registration form is displayed.
"""
def register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'sender'
            user.save()
            msg = 'user created'

            dashboard_mapping = {
                'sender': 'sender_dashboard',
            }
            dashboard_url = dashboard_mapping.get(user.role)
            user.backend = 'django.contrib.auth.backends.ModelBackend'

            login(request, user)
            
            return redirect(dashboard_url)

        else:
            msg = 'form is not valid'
    else:
        form = SignUpForm()
    return render(request,'auth/register.html', {'form': form, 'msg': msg})

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