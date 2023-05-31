from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect

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

def register_package(request):
    return render(request, 'register_package.html', {})

def logout_user(request):
    logout(request)
    return redirect('logout.html/')
