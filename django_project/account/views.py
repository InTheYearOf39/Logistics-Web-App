from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, LoginForm
from django.shortcuts import render
from .forms import PackageForm
from .models import Package
from django.contrib.auth.decorators import login_required
import random
import string
from .utils import get_time_of_day
from account.models import User
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse

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

def riders(request):
    couriers = User.objects.filter(role='courier')  # Retrieve only the couriers from the database
    
    context = {
        'couriers': couriers
    }
    return render(request, 'admin/riders.html', context)

def users(request):
    users = User.objects.all()  # Retrieve all users from the database
    
    context = {
        'users': users
    }
    
    return render(request, 'admin/users.html', context)


def assign_courier(request, package_id):
    package = get_object_or_404(Package, id=package_id)
    
    if request.method == 'POST':
        courier_id = request.POST.get('courier')
        courier = get_object_or_404(User, id=courier_id, role='courier')
        
        previous_courier_status = courier.status  # Save the previous status
        
        package.courier = courier
        package.status = 'ongoing'  # Update the status to "ongoing"
        package.save()
        
        # Update the courier status to "on-trip" only if they were not already on-trip
        if previous_courier_status != 'on-trip':
            courier.status = 'on-trip'
            courier.save()
        
        return redirect('admin_dashboard')  # Redirect back to the admin dashboard or any desired page
    
    couriers = User.objects.filter(role='courier')
    
    return render(request, 'admin/assign_courier.html', {'package_id': package_id, 'couriers': couriers})

# def assign_courier(request, package_id):
#     package = get_object_or_404(Package, id=package_id)
    
#     if request.method == 'POST':
#         courier_id = request.POST.get('courier')
#         courier = get_object_or_404(User, id=courier_id, role='courier')
        
#         package.courier = courier
#         package.status = 'ongoing'  # Update the status to "ongoing"
#         package.save()
        
#         return redirect('admin_dashboard')  # Redirect back to the admin dashboard or any desired page
    
#     couriers = User.objects.filter(role='courier')
    
#     return render(request, 'admin/assign_courier.html', {'package': package, 'couriers': couriers})


def admin(request):
    packages = Package.objects.filter(
        Q(status='ongoing') | Q(status='upcoming')
    )
    greeting_message = get_time_of_day()
    context = {
        'greeting_message': greeting_message,
        'packages': packages
    }
    return render(request, 'admin/admin_dashboard.html', context)

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
    greeting_message = get_time_of_day()
    context = {
        'greeting_message': greeting_message
    }
    return render(request, 'recipient_dashboard.html', context)

def courier_dashboard(request):
    greeting_message = get_time_of_day()
    context = {
        'greeting_message': greeting_message
    }
    return render(request, 'courier_dashboard.html', context)


def register_package(request):
    return render(request, 'register_package.html', {})

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
                # 'admin': 'admin_dashboard',
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
                        'admin': 'admin_dashboard',
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
            package.delivery_number = package._generate_delivery_number()
            package.status = 'upcoming'
            package.save()
            return redirect('sender_dashboard')
        else:
            return HttpResponse(form.errors)
    else:
        form = PackageForm(initial={'courier': None})  # Exclude courier field from the form

    return render(request, 'register_package.html', {'form': form})

# def register_package(request):
#     if request.method == 'POST':
#         form = PackageForm(request.POST)
#         if form.is_valid():
#             package = form.save(commit=False)
#             package.user = request.user
#             package.delivery_number = generate_delivery_number()
#             package.status = 'upcoming'
#             package.save()
#             return redirect('sender_dashboard')
#         else:
#             error_message = 'Error processing your request'
#     else:
#         form = PackageForm()
#         error_message = None
    
#     return render(request, 'register_package.html', {'form': form, 'error_message': error_message})




