from django.shortcuts import render, redirect
from lmsapp.models import Package, User
from lmsapp.utils import get_time_of_day
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.contrib import messages
import random
from django.conf import settings



User = get_user_model()

@login_required
def drop_pick_zone_dashboard(request):
    drop_pick_zone = request.user
    packages = Package.objects.filter(dropOffLocation=drop_pick_zone, status__in=['upcoming', 'in_transit', 'at_pickup', 'ready_for_pickup'])
    greeting_message = get_time_of_day()
    context = {
        'greeting_message': greeting_message,
        'packages': packages,
    }
    return render(request, 'drop_pick_zone/drop_pick_zone_dashboard.html', context)

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

        send_mail(subject, message, settings.EMAIL_HOST_USER, [sender_email])

        return redirect('dpz_dispatch')

    return render(request, 'drop_pick_zone/drop_pick_dashboard.html', {'package': package})

def confirm_at_pickup(request, package_id):
    if request.method == 'POST':
        package = Package.objects.get(pk=package_id)

        # Generate OTP
        otp = random.randint(100000, 999999)

        # Save the OTP in the package
        package.otp = otp
        package.save()

        # Update the package status
        package.status = 'ready_for_pickup'
        package.save()

        courier = package.courier
        if courier:
            courier.status = 'available'
            courier.save()

        # Send the email with OTP
        subject = "Package Arrival Notification"
        message = f"Dear {package.recipientName},\n\nYour package with delivery number {package.package_number} has arrived at its destination.\n\nOTP: Your One Time Password is: {otp}, please do not share this with anyone but your courier.\n\nThank you,\nThe Courier Service Team"
        receiver = package.recipientEmail

        try:
            send_mail(subject, message, settings.EMAIL_HOST_USER, [receiver])
            messages.success(request, "Email notification sent successfully.")

            # # Update the status to 'arrived'
            # if package.status == 'pending_pickup':
            #     package.status = 'arrived'
            #     package.save()
        except Exception as e:
            messages.error(request, "Failed to send email notification. Please try again later.")

        return redirect('drop_pick_zone_dashboard')  # Replace with the appropriate URL for the warehouse dashboard
    else:
        messages.error(request, "Invalid request.")

    return redirect('drop_pick_zone_dashboard')  # Replace with the appropriate URL for the warehouse dashboard

def confirm_recipient_pickup(request, package_id):
    if request.method == 'POST':
        package = Package.objects.get(pk=package_id)
        entered_code = request.POST.get('inputField')

        if package.status == 'ready_for_pickup' and package.otp == entered_code:
            package.status = 'completed'
            package.save()
            messages.success(request, "Package delivery confirmed successfully.")
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return redirect('drop_pick_zone_dashboard')


# def confirm_at_pickup(request, package_id):
#     package = get_object_or_404(Package, id=package_id)
#     package.status = 'ready_for_pickup'
#     package.save()

#     # Generate a 3-digit OTP
#     otp = str(random.randint(100000, 999999))
#     # Save the OTP in the package
#     package.otp = otp
#     package.save()
    
#     courier = package.courier
#     if courier:
#         courier.status = 'available'
#         courier.save()

#     # Send email to recipient
#     subject = 'Package Ready for Pickup'
#     message = f'Dear recipient, your package with delivery number {package.package_number} is ready for pickup at {package.dropOffLocation}.\n\n' \
#               f'Please provide the following OTP when picking up the package: {otp}.\n\n' \
#               f'Thank you.'
#     recipient_email = package.recipientEmail
#     send_mail(subject, message, 'sender@example.com', [recipient_email])

#     # Redirect to the desired page after confirming the pickup
#     return redirect('drop_pick_zone_dashboard')

# def confirm_recipient_pickup(request, package_id):
#     if request.method == 'POST':
#         package = Package.objects.get(pk=package_id)
#         entered_code = request.POST.get('inputField')

#         if package.status == 'ready_for_pickup' and package.otp == entered_code:
#             package.status = 'completed'
#             package.save()
#             messages.success(request, "Package delivery confirmed successfully.")
#         else:
#             messages.error(request, "Invalid OTP. Please try again.")
            
#         # courier = package.courier
#         # if courier:
#         #     courier.status = 'available'
#         #     courier.save()

#     return redirect('drop_pick_zone_dashboard')

def dispatch(request):
    drop_pick_zone = request.user
    packages = Package.objects.filter(dropOffLocation=drop_pick_zone, status='dropped_off')
    
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

        send_mail(subject, message, settings.EMAIL_HOST_USER, [sender_email])

        return redirect('dispatched_packages')

    return render(request, 'drop_pick_zone/drop_pick_dashboard.html', {'package': package})

def delivery_courier(request, package_id):
    package = get_object_or_404(Package, id=package_id)

    if request.method == 'POST':
        courier_id = request.POST.get('courier')
        courier = get_object_or_404(User, id=courier_id, role='courier')

        previous_courier_status = courier.status  # Save the previous status

        package.courier = courier

        # Update the package status based on the delivery type
        if (package.status == 'pending_delivery'):
            package.status = 'out_for_delivery'
        # elif package.deliveryType == 'premium' and package.status == 'upcoming':
        #     package.status = 'ongoing'

        package.save()
        
        # Check if the courier has any packages assigned
        has_packages = Package.objects.filter(courier=courier).exists()

        # Update the courier status
        if has_packages:
            courier.status = 'on-trip'
        else:
            courier.status = 'available'
        
        courier.save()


        return redirect('drop_pick_zone_dashboard')

    couriers = User.objects.filter(role='courier', status='available')  # Filter couriers by status='available'
    context = {
        'package_id': package_id,
        'couriers': couriers
        }
    
    return render(request, 'drop_pick_zone/delivery_courier.html', context)


def confirm_pickedup(request, package_id):
    if request.method == 'POST':
        package = Package.objects.get(pk=package_id)
        package.status = 'ongoing'
        package.save()
    
    return redirect('drop_pick_zone_dashboard')  # Replace with the appropriate URL for the warehouse dashboard
