from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, LoginForm
from django.shortcuts import render
from .forms import PackageForm
from .models import Package, Notification, OfflineNotification
from django.http import JsonResponse


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

def dashboard(request):
    return render(request, 'dashboard.html', {})

def recipient_dashboard(request):
    return render(request, 'recipient_dashboard.html', {})

def sender_dashboard(request):
    return render(request, 'sender_dashboard.html', {})

def courier_dashboard(request):
    return render(request, 'courier_dash.html', {})

def completed_package(request):
    return render(request, 'completed_package.html', {})

def register_package(request):
    return render(request, 'register_package.html', {})

def get_notification_count(request):
    # Get the current user
    user = request.user

    # Retrieve the count of unread notifications for the user
    notification_count = Notification.objects.filter(user=user, is_read=False).count()

    # Send notifications dynamically based on package status
    if user.role == 'recipient':
        # Get the packages where the recipient is the current user
        packages = Package.objects.filter(recipient=user)

        # Loop through the packages and check the status
        for package in packages:
            if package.status == 'completed' and not package.notification_sent:
                # Create a notification message for completed packages
                message = f"The package '{package.packageName}' has been delivered."

                # Check if the user is online
                if user.is_online:
                    # Create a notification and associate it with the recipient user
                    notification = Notification.objects.create(user=user, message=message)
                else:
                    # Create an offline notification and associate it with the recipient user
                    offline_notification = OfflineNotification.objects.create(user=user, message=message)

                # Set the package's notification_sent field to True to prevent duplicate notifications
                package.notification_sent = True
                package.save()

    context = {
        'notification_count': notification_count
    }

    return render(request, 'notification_count.html', context)


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
            return redirect('dashboard')
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

def register_package(request):
    if request.method == 'POST':
        form = PackageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sender_dashboard')
    else:
        form = PackageForm()
    
    packages = Package.objects.all()  # Retrieve all packages from the database
    
    return render(request, 'sender_dashboard.html', {'form': form, 'packages': packages})


def delivered_packages_api(request):
    delivered_packages = Package.objects.filter(status='Completed')

    # Create a list to hold the package data
    package_list = []
    for package in delivered_packages:
        package_data = {
            'number': package.pk,
            'title': package.packageName,
            'deliveringTo': package.recipientName,
            'status': package.status,
        }
        package_list.append(package_data)

    return JsonResponse(package_list, safe=False)


