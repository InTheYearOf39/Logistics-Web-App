from django.shortcuts import render


def index(request):
    return render(request, 'index.html', {})

def about(request):
    return render(request, 'about.html', {})

def services(request):
    return render(request, 'services.html', {})

def contact(request):
    return render(request, 'contact.html', {})

def home(request):
    return render(request, 'home.html', {})

def handle_404(request, exception):
    return render(request, '404.html', status=404)

def handle_500(request):
    return render(request, '500.html', status=500)

def handle_403(request, exception):
    return render(request, '403.html', status=403)

def handle_400(request, exception):
    return render(request, '400.html', status=400)

def home_register(request):
    return render(request, 'home_register.html', {})

def master_dashboard(request):
    return render(request, 'admin/master_dashboard.html', {})