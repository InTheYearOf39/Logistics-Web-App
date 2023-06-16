from django.shortcuts import render, redirect
from account.models import Package, User
from account.utils import get_time_of_day
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def drop_pick_zone_dashboard(request):
    drop_pick_zone = request.user
    packages = Package.objects.filter(dropOffLocation=drop_pick_zone, status__in=['upcoming'])
    greeting_message = get_time_of_day()
    context = {
        'greeting_message': greeting_message,
        'packages': packages,
    }
    return render(request, 'drop_pick_zone/drop_pick_dashboard.html', context)

def confirm_drop_off(request, package_id):
    package = get_object_or_404(Package, id=package_id)

    if request.method == 'POST':
        # Update the package status to 'dropped_off'
        package.status = 'dropped_off'
        package.save()

        # Send an email notification to the sender
        subject = 'Package Dropped Off'
        message = f'Dear sender, your package with delivery number {package.package_number} has been dropped off at {package.dropOffLocation}.'

        sender_user = User.objects.get(username=package.user.username)
        sender_email = sender_user.email

        send_mail(subject, message, sender_email, [sender_email])

        return redirect('dpz_dispatch')

    return render(request, 'drop_pick_zone/drop_pick_dashboard.html', {'package': package})

def dispatch(request):
    drop_pick_zone = request.user
    packages = Package.objects.filter(dropOffLocation=drop_pick_zone, status__in=['dropped_off'])
    
    context = {
        'packages': packages,
    }
    return render(request, 'drop_pick_zone/dispatch.html', context)



def dispatched_packages(request):
    drop_pick_zone = request.user
    packages = Package.objects.filter(dropOffLocation=drop_pick_zone, status='dispatched')
    return render(request, 'drop_pick_zone/dispatched_packages.html', {'packages': packages})


def confirm_pickup(request, package_id):
    package = get_object_or_404(Package, id=package_id)

    if request.method == 'POST':
        # Update the package status to 'en_route'
        package.status = 'en_route'
        package.save()

        # Send an email notification to the sender
        subject = 'Package Update: En Route to Warehouse'
        message = f'Dear Sender, your package {package.package_number} is now en route to the warehouse.'

        sender_user = User.objects.get(username=package.user.username)
        sender_email = sender_user.email

        send_mail(subject, message, sender_email, [sender_email])

        return redirect('dispatched_packages')

    return render(request, 'drop_pick_zone/drop_pick_dashboard.html', {'package': package})