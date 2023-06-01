from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, LoginForm
from django.shortcuts import render
from .forms import PackageForm
from .models import Package

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

# def register_package(request):
#     if request.method == 'POST':
#         form = PackageForm(request.POST)
#         if form.is_valid():
#             packageName = form.cleaned_data['packageName']
#             packageDescription = form.cleaned_data['packageDescription']
#             recipientName = form.cleaned_data['recipientName']
#             recipientAddress = form.cleaned_data['recipientAddress']
#             sendersAddress = form.cleaned_data['sendersAddress']
#             status = form.cleaned_data['status']
            
#             # Save the data to the Package model
#             package = Package(
#                 packageName=packageName,
#                 packageDescription=packageDescription,
#                 recipientName=recipientName,
#                 recipientAddress=recipientAddress,
#                 sendersAddress=sendersAddress,
#                 status=status
#             )
#             package.save()
            
#             return redirect('dashboard')  # Replace 'dashboard' with the appropriate URL pattern name for your dashboard view
#     else:
#         form = PackageForm()
#     return render(request, 'register_package.html', {'form': form})



def register_package(request):
    if request.method == 'POST':
        form = PackageForm(request.POST)
        if form.is_valid():
            form.save()
            # Optionally, you can perform additional actions with the saved package object
            return redirect('dashboard')  # Redirect to the dashboard page
    else:
        form = PackageForm()
    
    return render(request, 'register_package.html', {'form': form})


# def register_package(request):
#     if request.method == 'POST':
#         form = PackageForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('dashboard')  # Replace 'dashboard' with the appropriate URL pattern name for your dashboard view
#     else:
#         form = PackageForm()
#     return render(request, 'register_package.html', {'form': form})
