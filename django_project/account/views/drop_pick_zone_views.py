from django.shortcuts import render, redirect
from account.models import Package, User
from account.utils import get_time_of_day
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.core.mail import send_mail


@login_required
def drop_pick_zone_dashboard(request):
    drop_pick_zone = request.user
    packages = Package.objects.filter(dropOffLocation=drop_pick_zone)
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
        message = f'Your package with delivery number {package.package_number} has been dropped off at {package.dropOffLocation}.'
        sender_email = 'sender@example.com'
        recipient_email = package.recipientEmail  # Assuming the sender's email is stored in the package's recipientEmail field

        send_mail(subject, message, sender_email, [recipient_email])

        # return redirect('drop_pick_zone_dashboard')

    return render(request, 'drop_pick_zone/drop_pick_dashboard.html', {'package': package})








