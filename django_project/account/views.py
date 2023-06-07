from django.shortcuts import render, redirect, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q, Case, When, IntegerField
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, LoginForm
from .utils import get_time_of_day, generate_one_time_pin
from .forms import PackageForm
from .models import Package, User
import random
import string
from .utils import get_time_of_day
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings



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
        package.status = 'ongoing'
        package.save()
        

        # Update the courier status to "on-trip" only if they were not already on-trip
        if previous_courier_status != 'on-trip':
            courier.status = 'on-trip'
            courier.save()
        
        return redirect('admin_dashboard')  

    
    couriers = User.objects.filter(role='courier')
    
    return render(request, 'admin/assign_courier.html', {'package_id': package_id, 'couriers': couriers})


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

def admin(request):
    packages = Package.objects.filter(
        Q(status='ongoing') | Q(status='upcoming')
    ).order_by(
        Case(
            When(status='upcoming', then=0),
            When(status='ongoing', then=1),
            default=2,
            output_field=IntegerField()
        ),
        '-assigned_at'  # Sort by assignment day in descending order
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
    assigned_packages = Package.objects.filter(courier=request.user, status__in=['ongoing', 'completed'])
    greeting_message = get_time_of_day()
    context = {
        'greeting_message': greeting_message,
        'assigned_packages': assigned_packages,
    }
    return render(request, 'courier_dashboard.html', context)




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
            package.delivery_number = generate_delivery_number()
            
            # Check if the selected courier is already assigned to a package
            courier = package.courier
            if courier and courier.assigned_packages.exists():
                messages.error(request, 'Selected courier is already assigned to a package.')
                return redirect('register_package')
            
            package.status = 'upcoming'
            package.save()
            return redirect('sender_dashboard')
        else:
            error_message = 'Error processing your request'
    else:
        form = PackageForm()
        error_message = None

    return render(request, 'register_package.html', {'form': form, 'error_message': error_message})


def notify_arrival(request, package_id):
    # Retrieve the package object
    package = Package.objects.get(pk=package_id)

    # Generate OTP
    otp = random.randint(100000, 999999)

    # Send the email with OTP
    subject = "Package Arrival Notification"
    message = f"Dear {package.recipientName},\n\nYour package with delivery number {package.delivery_number} has arrived at its destination.\n\nOTP: Your One Time Password is: {otp}, please do not share this to anyone but your courier.\n\nThank you,\nThe Courier Service Team"
    sender = settings.EMAIL_HOST_USER
    receiver = package.recipientEmail

    try:
        send_mail(subject, message, sender, [receiver])
        messages.success(request, "Email notification sent successfully.")
    except Exception as e:
        messages.error(request, "Failed to send email notification. Please try again later.")

    return redirect('courier_dashboard')  # Replace with the appropriate URL

# def notify_arrival(request, package_id):
#     # Retrieve the package object
#     package = Package.objects.get(pk=package_id)

#     # Send the email
#     subject = "Package Arrival Notification"
#     message = f"Dear {package.recipientName},\n\nYour package with delivery number {package.delivery_number} has arrived at its destination.\n\nThank you,\nThe Courier Service Team"
#     sender = "<blessingisrael625@gmail.com>"  # Replace with your email address
#     receiver = package.recipientEmail

#     try:
#         send_mail(subject, message, sender, [receiver])
#         messages.success(request, "Email notification sent successfully.")
#     except Exception as e:
#         messages.error(request, "Failed to send email notification. Please try again later.")

#     return redirect('courier_dashboard')  # Replace with the appropriate URL