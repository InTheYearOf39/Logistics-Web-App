from django.shortcuts import render, redirect, redirect
from account.models import Package, User
import random
from account.utils import get_time_of_day
from django.shortcuts import redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings



def courier_dashboard(request):
    assigned_packages = Package.objects.filter(courier=request.user, status__in=['dispatched', 'ongoing', 'arrived','completed'])
    greeting_message = get_time_of_day()
    context = {
        'greeting_message': greeting_message,
        'assigned_packages': assigned_packages,
    }
    return render(request, 'courier/courier_dashboard.html', context)

def notify_arrival(request, package_id):
    # Retrieve the package object
    package = Package.objects.get(pk=package_id)

    # Generate OTP
    otp = random.randint(100000, 999999)

    # Save the OTP in the package
    package.otp = otp
    package.save()

    # Send the email with OTP
    subject = "Package Arrival Notification"
    message = f"Dear {package.recipientName},\n\nYour package with delivery number {package.package_number} has arrived at its destination.\n\nOTP: Your One Time Password is: {otp}, please do not share this with anyone but your courier.\n\nThank you,\nThe Courier Service Team"
    sender = settings.EMAIL_HOST_USER
    receiver = package.recipientEmail

    try:
        send_mail(subject, message, sender, [receiver])
        messages.success(request, "Email notification sent successfully.")

        # Update the status to 'arrived'
        if package.status == 'ongoing':
            package.status = 'arrived'
            package.save()
    except Exception as e:
        messages.error(request, "Failed to send email notification. Please try again later.")

    return redirect('courier_dashboard')  # Replace with the appropriate URL

def confirm_delivery(request, package_id):
    if request.method == 'POST':
        package = Package.objects.get(pk=package_id)
        entered_code = request.POST.get('inputField')

        if package.status == 'arrived' and package.otp == entered_code:
            package.status = 'completed'
            package.save()
            messages.success(request, "Package delivery confirmed successfully.")
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return redirect('courier_dashboard')  # Replace with the appropriate URL

def courier_history(request):
    assigned_packages = Package.objects.filter(courier=request.user, status__in=['completed'])
    greeting_message = get_time_of_day()
    context = {
        'greeting_message': greeting_message,
        'assigned_packages': assigned_packages,
    }
    return render(request, 'courier/courier_history.html', context)