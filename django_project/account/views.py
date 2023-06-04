from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserChangeForm
from .forms import CustomUserCreationForm, UserEditForm
from .forms import SignUpForm, LoginForm
from django.shortcuts import render
from .forms import PackageForm
from .models import Package, User, UserManagement
from django.contrib.auth.decorators import login_required
import random
import string
from .utils import get_time_of_day


def base(request):
    return render(request, 'base.html', {})

def index(request):
    return render(request, 'index.html', {})

def about(request):
    return render(request, 'about.html', {})

def services(request):
    return render(request, 'services.html', {})

def contact(request):
    return render(request, 'contact.html', {})

@login_required
def sender_dashboard(request):
    greeting_message = get_time_of_day()
    packages = request.user.packages.all()
    context = {
        'greeting_message': greeting_message,
        'packages': packages
    }
    return render(request, 'sender_dashboard.html', context)

def recipient_dashboard(request):
    return render(request, 'recipient_dashboard.html', {})

def courier_dashboard(request):
    greeting_message = get_time_of_day()
    context = {
        'greeting_message': greeting_message
    }
    return render(request, 'courier_dashboard.html', context)


def completed_pack(request):
    return render(request, 'completed_pack.html', {})

def completed_packages(request):
    completed_packages = Package.objects.filter(status='completed')
    return render(request, 'completed_packages.html', {'completed_packages': completed_packages})

def register_package(request):
    return render(request, 'register_package.html', {})

def admin_dashboard(request):
    return render(request, 'admin_dashboard.html', {})

def user_management(request):
    users = User.objects.all()

    context = {
        'users': users
    }

    return render(request, 'user_management.html', context)

def logout_user(request):
    logout(request)
    return redirect('logout.html/')

def register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            msg = 'user created'

            dashboard_mapping = {
                'courier': 'courier_dashboard',
                'sender': 'sender_dashboard',
                'recipient': 'recipient_dashboard',
            }
            dashboard_url = dashboard_mapping.get(user.role)
            login(request, user)
            
            return redirect(dashboard_url)

        else:
            msg = 'form is not valid'
    else:
        form = SignUpForm()
    return render(request,'register.html', {'form': form, 'msg': msg})


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
                        'courier': 'courier_dashboard',
                        'sender': 'sender_dashboard',
                        'recipient': 'recipient_dashboard',
                    }
                dashboard_url = dashboard_mapping.get(user.role)
                if dashboard_url:
                    return redirect(dashboard_url)
            else:
                msg= 'invalid credentials'
        else:
            msg = 'error validating form'
    return render(request, 'login.html', {'form': form, 'msg': msg})

def generate_delivery_number():
    prefix = 'dn'
    digits = ''.join(random.choices(string.digits, k=5))
    return f'{prefix}{digits}'

def register_package(request):
    if request.method == 'POST':
        form = PackageForm(request.POST)
        if form.is_valid():
            package = form.save(commit=False)
            package.user = request.user
            package.delivery_number = generate_delivery_number()
            package.status = 'upcoming'
            package.save()
            return redirect('sender_dashboard')
        else:
            error_message = 'Error processing your request'
    else:
        form = PackageForm()
        error_message = None
    
    return render(request, 'register_package.html', {'form': form, 'error_message': error_message})


def couriers(request):
    available_riders = Package.objects.filter(status='upcoming', user__isnull=False)
    in_transit_riders = Package.objects.filter(status='ongoing', user__isnull=False)
    unavailable_riders = Package.objects.filter(status='completed', user__isnull=False)

    return render(request, 'couriers.html', {
        'available_riders': available_riders,
        'in_transit_riders': in_transit_riders,
        'unavailable_riders': unavailable_riders,
    })


def view_packages(request):
    ongoing_packages = Package.objects.filter(status='ongoing')
    completed_packages = Package.objects.filter(status='completed')
    upcoming_packages = Package.objects.filter(status='upcoming')
    new_packages = Package.objects.order_by('-id')[:10]  # Example: Get the 10 latest packages

    return render(request, 'view_packages.html', {
        'ongoing_packages': ongoing_packages,
        'completed_packages': completed_packages,
        'upcoming_packages': upcoming_packages,
        'new_packages': new_packages,
    })

def create_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user registration form
            # Create a user management entry for the created user
            user_management = UserManagement(username=user.username, email=user.email, role=user.role)
            user_management.save()
            return redirect('user_management')  # Redirect to the user management page
    else:
        form = CustomUserCreationForm()

    context = {
        'form': form
    }
    return render(request, 'create_user.html', context)

def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_management')  # Redirect to the user management page
    else:
        form = UserEditForm(instance=user)

    context = {
        'form': form
    }

    return render(request, 'edit_user.html', context)

def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        user.delete()
        return redirect('user_management')

    return render(request, 'delete_user.html', {'user': user})

