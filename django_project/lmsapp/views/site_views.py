from django.shortcuts import render

#Renders out the 'index.html' template
def index(request):
    return render(request, 'index.html', {})

#Renders out the 'about.html' template
def about(request):
    return render(request, 'about.html', {})

#Renders out the 'services.html' template
def services(request):
    return render(request, 'services.html', {})

#Renders out the 'contact.html' template
def contact(request):
    return render(request, 'contact.html', {})