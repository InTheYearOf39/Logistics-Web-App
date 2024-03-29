from django.shortcuts import render, redirect
from lmsapp.models import Package, User, DropPickZone
from lmsapp.forms import PackageForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, get_object_or_404
from django.core.mail import send_mail, EmailMessage, BadHeaderError
from django.contrib.auth import get_user_model
from django.contrib import messages
import random
import string
from django.conf import settings
import os
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
import math
from django.http import JsonResponse
import math
from lmsapp.utils import send_sms
from django.db.models import Q
from lmsapp.tasks import send_email_notification

def is_drop_pick_user(user):
    return user.role == 'drop_pick_zone'


User = get_user_model()

""" 
The view displays the dashboard for a drop pick zone. It retrieves the packages assigned to the drop pick zone with specific statuses and renders them in the 'drop_pick_zone/drop_pick_zone_dashboard.html' template.
"""
@login_required
@user_passes_test(is_drop_pick_user)
def drop_pick_zone_dashboard(request):
    drop_pick_zone = DropPickZone.objects.get(users=request.user)
    packages = Package.objects.filter(
        (
            Q(dropOffLocation=drop_pick_zone, status__in=['upcoming', 'in_transit']) |
            Q(recipientPickUpLocation=drop_pick_zone, status__in=['at_pickup', 'ready_for_pickup'])
        )
    )
    context = {
        'packages': packages,
    }
    return render(request, 'drop_pick_zone/drop_pick_zone_dashboard.html', context)



""" 
the view enables a drop_pick_zone user to confirm the drop-off of a package at the drop_pick_zone. 
When the user submits the confirmation form, the package status is updated to 'dropped_off', 
and an email notification is sent to the sender.
"""
@login_required
@user_passes_test(is_drop_pick_user)
def confirm_drop_off(request, package_id):
    package = get_object_or_404(Package, id=package_id)

    if request.method == 'POST':
        # Update the package status to 'dropped_off'
        package.status = 'dropped_off'
        package.save()

        # Send an email notification to the sender
        subject = 'Package Dropped Off'
        message = f'Dear Customer, your package with delivery number {package.package_number} has been dropped off at {package.dropOffLocation}.'

        sender_user = User.objects.get(username=package.user.username)
        sender_email = sender_user.email

        # Create an EmailMessage instance
        email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [sender_email])

        # Get the path to the image
        # image_path = os.path.join(settings.STATIC_ROOT, 'img', 'DroppedOff.png')

        # # Check if the image file exists
        # if os.path.isfile(image_path):
        #     # Attach the image to the email
        #     with open(image_path, 'rb') as image_file:
        #         email.attach_file(image_path, 'image/png')

        # Send the email
        email.send()

        messages.success(request, f'{package.packageName} package drop off confirmed successfully.')
        return redirect('received_packages')

    return render(request, 'drop_pick_zone/drop_pick_dashboard.html', {'package': package})

""" 
The view enables a user to confirm that a package is ready for pickup by a recipient. 
When the user submits the confirmation form, an OTP is generated and saved in the package, 
the package status is updated, and an email notification with the OTP is sent to the recipient.
""" 
@login_required
@user_passes_test(is_drop_pick_user)
def confirm_at_pickup(request, package_id):
    if request.method == 'POST':
        package = Package.objects.get(pk=package_id)

        # Generate OTP
        otp = random.randint(100000, 999999)

        # Save the OTP in the package
        package.otp = otp

        # Update the package status
        package.status = 'ready_for_pickup'
        package.save()

        courier = package.courier
        if courier:
            courier.status = 'available'
            courier.save()

        # Send the email with OTP
        subject = "Package Arrival Notification"
        message_receiver = f"Dear {package.recipientName},\n\nYour package with delivery number {package.package_number} has arrived at its destination.\n\nOTP: Your One Time Password is: {otp}, please do not share this with anyone but your courier.\n\nThank you,\nThe Courier Service Team"
        message_sender = f"Dear Customer,\n\nThe package with delivery number {package.package_number} has arrived at the pick-up location.\n\nThank you,\nThe Courier Service Team."
        sender_user = User.objects.get(username=package.user.username)
        receiver = package.recipientEmail

        recipient_contact = str(package.recipientTelephone).strip()

        if len(recipient_contact) == 10 and recipient_contact.startswith('0'):
            recipient_contact = '+256' + recipient_contact[1:]

        send_sms([recipient_contact], message_receiver, settings.AFRICASTALKING_SENDER)

        try:
            # send_mail(subject, message_receiver, settings.EMAIL_HOST_USER, [receiver])
            # send_mail(subject, message_sender, settings.EMAIL_HOST_USER, [sender_user.email])

            send_email_notification.apply_async((subject, message_receiver, receiver))
            send_email_notification.apply_async((subject, message_sender, sender_user.email))
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


""" 
The view confirms the recipient's pickup of a package from the drop_pick_zone by comparing the entered OTP 
with the one stored in the package. I the OTP matches and the package status is 'ready_for_pickup', 
the package status is updated to 'completed'
"""
@login_required
@user_passes_test(is_drop_pick_user)
def confirm_recipient_pickup(request, package_id):
    if request.method == 'POST':
        package = Package.objects.get(pk=package_id)
        entered_code = request.POST.get('inputField')

        if package.status == 'ready_for_pickup' and str(package.otp) == entered_code:
            package.status = 'completed'
            package.save()
            messages.success(request, "Package delivery confirmed successfully.")
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return redirect('drop_pick_zone_dashboard')


"""
The view retrieves the packages dropped off at the current drop pick zone and displays them in the dispatch template. 
The retrieved packages are passed to the template through the context.
"""
@login_required
@user_passes_test(is_drop_pick_user)
def received_packages(request):
    # drop_pick_zone = request.user
    drop_pick_zone = DropPickZone.objects.get(users=request.user)
    packages = Package.objects.filter(dropOffLocation=drop_pick_zone, status='dropped_off')
    
    context = {
        'packages': packages,
    }
    return render(request, 'drop_pick_zone/received_packages.html', context)


""" 
The view retrieves packages that are marked as 'dispatched' and belong to the current drop pick zone user. 
It then renders the dispatched_packages.html template, passing the retrieved packages to be displayed.
"""
@login_required
@user_passes_test(is_drop_pick_user)
def dispatched_packages(request):
    # drop_pick_zone = request.user
    drop_pick_zone = DropPickZone.objects.get(users=request.user)
    packages = Package.objects.filter(dropOffLocation=drop_pick_zone, status='dispatched')
    return render(request, 'drop_pick_zone/dispatched_packages.html', {'packages': packages})

""" 
The view allows the drop pick zone to confirm the pickup of a package. Upon confirmation, 
the package status is updated and an email notification is sent to the sender. 
"""
@login_required
@user_passes_test(is_drop_pick_user)
def confirm_pickup(request, package_id):
    package = get_object_or_404(Package, id=package_id)

    if request.method == 'POST':
        # Update the package status to 'en_route'
        package.status = 'en_route'
        package.save()
        


        # Send an email notification to the sender
        subject = 'Package Update: En Route to Warehouse'
        message = f'Dear Customer, your package {package.package_number} is now en route to the warehouse.'

        sender_user = User.objects.get(username=package.user.username)
        sender_email = sender_user.email

        # send_mail(subject, message, settings.EMAIL_HOST_USER, [sender_email])
        send_email_notification.apply_async((subject, message, sender_email))

        messages.success(request, "Package collection by courier confirmed successfully.")
        return redirect('dispatched_packages')

    return render(request, 'drop_pick_zone/drop_pick_dashboard.html', {'package': package})

def generate_package_number():
    prefix = 'PN'
    digits = ''.join(random.choices(string.digits, k=5))
    return f'{prefix}{digits}'

@login_required
@xframe_options_exempt 
@user_passes_test(is_drop_pick_user)
def add_package_droppick(request):
    user_drop_pick_zone = None
    
    senders = User.objects.filter(role='sender')
    if request.method == 'POST':
        form = PackageForm(request.POST)

        if form.is_valid():
            package = form.save(commit=False)

            # Automatically set the dropOffLocation to the one the user belongs to
            user_drop_pick_zone = request.user.drop_pick_zone

            delivery_type = request.POST.get('deliveryType')
            recipient_latitude = request.POST.get('recipient_latitude')
            recipient_longitude = request.POST.get('recipient_longitude')

            package.sendersName = form.cleaned_data["sendersName"]
            package.sendersEmail = form.cleaned_data["sendersEmail"]
            package.sendersContact = form.cleaned_data["sendersContact"]
            package.packageName = form.cleaned_data["packageName"]
            package.packageDescription = form.cleaned_data["packageDescription"]
            package.deliveryType = delivery_type
            package.dropOffLocation = user_drop_pick_zone
            package.recipientName = form.cleaned_data["recipientName"]
            package.recipientEmail = form.cleaned_data["recipientEmail"]
            package.recipientTelephone = form.cleaned_data["recipientTelephone"]
            package.recipientAddress = form.cleaned_data["recipientAddress"]
            package.recipientIdentification = form.cleaned_data["recipientIdentification"]
            package.genderType = form.cleaned_data["genderType"]
            package.recipientPickUpLocation = form.cleaned_data["recipientPickUpLocation"]
            package.user = request.user
            package.recipient_latitude = recipient_latitude
            package.recipient_longitude = recipient_longitude
            package.package_number = generate_package_number()
            package.created_by = request.user

            package.status = 'dropped_off'

            selected_user_id = request.POST.get('user')
            if selected_user_id:
                selected_user = User.objects.get(id=selected_user_id)

                package.sendersEmail = selected_user.email
                package.sendersName = selected_user.username
            package.save()


            subject = 'Package Registered'
            message = (
                f"Dear Customer, your package has been successfully registered.\n\n"
                f"Package Number: {package.package_number}\n"
                f"Recipient: {package.recipientName}\n"
                f"Recipient Address: {package.recipientAddress}\n"
                f"If you have any questions, please contact our customer support team.\n"
            )

            if package.dropOffLocation:
                message += f"Drop-off Location: {package.dropOffLocation.name}\n"

            message += f"Status: {package.status}"
            
            # from_email = settings.DEFAULT_FROM_EMAIL
            # recipient_list = [package.recipientEmail, package.sendersEmail]
                           
            sender_contact = str(package.sendersContact).strip()

            if len(sender_contact) == 10 and sender_contact.startswith('0'):
                sender_contact = '+256' + sender_contact[1:]

            send_sms([sender_contact], message, "LASTMILE-PUDONET")

            try:    
                # send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                send_email_notification.apply_async((subject, message, package.recipientEmail))
                send_email_notification.apply_async((subject, message, package.sendersEmail))
            except BadHeaderError as e:
                # Handle the BadHeaderError
                print("Error: BadHeaderError:", str(e))
            except Exception as e:
                # Handle other exceptions
                print("Error:", str(e))

            messages.success(request, f'The package: {package.packageName} for {package.sendersName} has been registered successfully')
            return redirect('received_packages')
        else:
            drop_pick_zones = DropPickZone.objects.all()
            context = { 'form': form, 'user_drop_pick_zone': request.user.drop_pick_zone, 'drop_pick_zones': drop_pick_zones }
            return render(request, 'drop_pick_zone/add_package.html', context)

    else:
        form = PackageForm()
        user_drop_pick_zone = request.user.drop_pick_zone

        # Get the drop_pick_zones data to populate the recipientPickUpLocation dropdown
        drop_pick_zones = DropPickZone.objects.all()  
        context = {'form': form, 'drop_pick_zones': drop_pick_zones, 'user_drop_pick_zone': user_drop_pick_zone, 'senders': senders}
        return render(request, 'drop_pick_zone/add_package.html', context)


def calculate_distance(lat1, lon1, lat2, lon2):
    # Radius of the Earth in kilometers
    R = 6371.0

    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad

    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance


def calculate_distances(request):
    if request.method == 'POST':
        recipient_latitude = float(request.POST.get('recipient_latitude'))
        recipient_longitude = float(request.POST.get('recipient_longitude'))
        
        drop_pick_zones = DropPickZone.objects.all()
        
        distances = []
        for drop_pick_zone in drop_pick_zones:
            distance = calculate_distance(drop_pick_zone.latitude, drop_pick_zone.longitude, recipient_latitude, recipient_longitude)
            distances.append({'id': drop_pick_zone.id, 'name': drop_pick_zone.name, 'distance': distance})
        
        distances.sort(key=lambda x: x['distance'])
        return JsonResponse({'distances': distances})