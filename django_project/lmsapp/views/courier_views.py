from django.shortcuts import render, redirect, redirect
from lmsapp.models import Package
import random
from lmsapp.utils import get_time_of_day
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings



"""
A function to render the courier dashboard. It retrieves the assigned packages for the logged in courier 
and passes them to the template along with a greeting message. Relevant information is then displayed
to the courier on their dashboard.
"""
def courier_dashboard(request):
    assigned_packages = Package.objects.filter(courier=request.user, status__in=['dispatched', 'ongoing', 'arrived', 'en_route', 'warehouse_arrival', 'in_transit', 'at_pickup'])
    greeting_message = get_time_of_day()
    context = {
        'greeting_message': greeting_message,
        'assigned_packages': assigned_packages,
    }
    return render(request, 'courier/courier_dashboard.html', context)

"""
A function to handle the notification of package arrival at the warehouse. When the view is accessed with a POST request, 
the package is retrieved by it's package id and then the package status is updated to 'warehouse_arrival', An email notification is sent to the sender and the warehouse. If the request method is not POST, it displays an error message. Finally, the user is redirected to the courier dashboard.
 """
def notify_arrival(request, package_id):
    if request.method == 'POST':
        package = Package.objects.get(pk=package_id)
        package.status = 'warehouse_arrival'
        package.save()

        # Send email to sender
        sender_email = package.recipientEmail
        sender_message = f"Your package with ID {package.package_number} has arrived at the warehouse."
        send_mail('Package Arrival Notification', sender_message, settings.EMAIL_HOST_USER, [sender_email])

        # Send email to warehouse
        warehouse_email = 'warehouse@example.com'  # Replace with actual warehouse email
        warehouse_message = f"A package with ID {package.package_number} has arrived at the warehouse."
        send_mail('Package Arrival Notification', warehouse_message, settings.EMAIL_HOST_USER, [warehouse_email])

        messages.success(request, "Package arrival notified successfully.")
    else:
        messages.error(request, "Invalid request.")

    return redirect('courier_dashboard')  # Replace with the appropriate URL

"""
A function to handle the notification of package drop-off. When the view is accessed with a POST request, a package is retrieved by its id and it's status updated to 'at_pickup'. The user is then redirected to the courier dashboard.
"""
def notify_dropoff(request, package_id):
    
    if request.method == 'POST':
        package = get_object_or_404(Package, id=package_id)
        package.status = 'at_pickup'
        package.save()

        messages.success(request, "Package drop-off notified successfully.")
        return redirect('courier_dashboard')

    return render(request, 'notify_dropoff.html', {'package': package})

"""
A function to handle notifying the recipient of a package arrival by sending an email with the OTP. A package is retrieved by its package id, then a random integer is generated and stored in a variable 'otp'. The otp is then associated to the package and the package is saved, The email is then sent and the the package status is updated from 'ongoing' to 'arrived'. The user is then redirected to the courier dashboard.
 """
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
    receiver = package.recipientEmail

    try:
        send_mail(subject, message, settings.EMAIL_HOST_USER, [receiver])
        messages.success(request, "Email notification sent successfully.")

        # Update the status to 'arrived'
        if package.status == 'ongoing':
            package.status = 'arrived'
            package.save()
    except Exception as e:
        messages.error(request, "Failed to send email notification. Please try again later.")

    return redirect('courier_dashboard')

"""
A function to handle confirming the delivery of a package by checking the entered OTP. 
If the entered OTP matches the stored OTP and the package status is 'arrived', the package status is updated to 'completed', a success message is displayed, and the associated courier's status is updated from 'on-trip' to 'available. If the entered OTP is invalid, an error message is displayed. The user is then redirected to the courier dashboard.
"""
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

    return redirect('courier_dashboard')  

"""
A function to retrieve the completed packages assigned to the current courier and display them in the courier history template. i.e Packages with the status 'completed' The greeting message and the assigned packages are passed to the template through the context.
"""
def courier_history(request):
    assigned_packages = Package.objects.filter(courier=request.user, status__in=['completed'])
    greeting_message = get_time_of_day()
    context = {
        'greeting_message': greeting_message,
        'assigned_packages': assigned_packages,
    }
    return render(request, 'courier/courier_history.html', context)