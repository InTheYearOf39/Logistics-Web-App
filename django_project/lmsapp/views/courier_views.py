from django.shortcuts import render, redirect, redirect
from lmsapp.models import Package, User
import random
from lmsapp.utils import get_time_of_day
from django.shortcuts import redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings



def courier_dashboard(request):
    assigned_packages = Package.objects.filter(courier=request.user, status__in=['dispatched', 'ongoing', 'arrived','completed','ready_for_pickup' , 'en_route', 'warehouse_arrival', 'in_transit', 'at_pickup'])
    greeting_message = get_time_of_day()
    context = {
        'greeting_message': greeting_message,
        'assigned_packages': assigned_packages,
    }
    return render(request, 'courier/courier_dashboard.html', context)


def notify_arrival(request, package_id):
    if request.method == 'POST':
        package = Package.objects.get(pk=package_id)
        package.status = 'warehouse_arrival'
        package.save()

        # Send email to sender
        sender_email = package.recipientEmail
        sender_message = f"Your package with ID {package.package_number} has arrived at the warehouse."
        send_mail('Package Arrival Notification', sender_message, 'garynkuraiji@gmail.com', [sender_email])

        # Send email to warehouse
        warehouse_email = 'warehouse@example.com'  # Replace with actual warehouse email
        warehouse_message = f"A package with ID {package.package_number} has arrived at the warehouse."
        send_mail('Package Arrival Notification', warehouse_message, 'sender@example.com', [warehouse_email])

        messages.success(request, "Package arrival notified successfully.")
    else:
        messages.error(request, "Invalid request.")

    return redirect('courier_dashboard')  # Replace with the appropriate URL

def notify_pick_up(request, package_id):
    if request.method == 'POST':
        package = Package.objects.get(pk=package_id)
        package.status = 'at_pickup'
        package.save()

        # Send email to sender
        sender_email = package.recipientEmail
        sender_message = f"Your package with ID {package.package_number} has arrived at the warehouse."
        send_mail('Package Arrival Notification', sender_message, 'garynkuraiji@gmail.com', [sender_email])

        # Send email to warehouse
        warehouse_email = 'warehouse@example.com'  # Replace with actual warehouse email
        warehouse_message = f"A package with ID {package.package_number} has arrived at the warehouse."
        send_mail('Package Arrival Notification', warehouse_message, 'sender@example.com', [warehouse_email])

        messages.success(request, "Package arrival notified successfully.")
    else:
        messages.error(request, "Invalid request.")

    return redirect('courier_dashboard')  # Replace with the appropriate URL



def notify_recipient(request, package_id):
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
            
        courier = package.courier
        if courier:
            courier.status = 'available'
            courier.save()


    return redirect('courier_dashboard')  # Replace with the appropriate URL

def courier_history(request):
    assigned_packages = Package.objects.filter(courier=request.user, status__in=['completed'])
    greeting_message = get_time_of_day()
    context = {
        'greeting_message': greeting_message,
        'assigned_packages': assigned_packages,
    }
    return render(request, 'courier/courier_history.html', context)