from account.utils import get_time_of_day
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, redirect, get_object_or_404
from account.models import Package, User
from django.contrib import messages
from django.shortcuts import render, redirect
from account.forms import ChangePasswordForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail



@login_required
def warehouse_dashboard(request):
    greeting_message = get_time_of_day()
    # Retrieve the current warehouse user
    warehouse_user = request.user

    # Retrieve the drop_pick_zones belonging to the warehouse
    drop_pick_zones = User.objects.filter(role='drop_pick_zone', warehouse=warehouse_user)

    # Create an empty dictionary to store packages by location
    packages_by_location = {}

    # Iterate over the drop_pick_zones belonging to the warehouse
    for drop_pick_zone in drop_pick_zones:
        # Retrieve the packages dropped off at each drop_pick_zone
        packages = Package.objects.filter(dropOffLocation=drop_pick_zone, status='dropped_off')

        # Add the drop_pick_zone and associated packages to the dictionary
        packages_by_location[drop_pick_zone.name] = packages

    if request.method == 'POST':
        selected_packages = request.POST.getlist('selected_packages')
        courier_id = request.POST.get('courier')

        if selected_packages and courier_id:
            courier = get_object_or_404(User, id=courier_id, role='courier', status='available')

            # Update the packages with the assigned courier and change their status
            packages = Package.objects.filter(id__in=selected_packages)
            packages.update(courier=courier, status='dispatched')
            
            # courier_status = Package.objects.filter(courier=courier, status__in=['dispatched', 'upcoming', 'ongoing', 'arrived', 'en_route', 'warehouse_arrival', 'in_transit', 'at_pickup', 'ready_for_pickup']).exists()
            courier_status = Package.objects.filter(courier=courier, status='dispatched').exists()

            if courier_status:
                courier.status = 'on-trip'
            # else:
            #     courier.status = 'available'
            
            courier.save()

            messages.success(request, 'Packages successfully assigned to courier.')

            return redirect('warehouse_dashboard')

    available_couriers=User.objects.filter(role='courier', status='available')
    context = {
        'packages_by_location': packages_by_location,
        'greeting_message': greeting_message,
        'available_couriers': available_couriers
    }

    return render(request, 'warehouse/warehouse_dashboard.html', context)

@login_required
# def change_password(request):
#     if request.method == 'POST':
#         form = ChangePasswordForm(request.user, request.POST)
#         if form.is_valid():
#             user = form.save()
#             update_session_auth_hash(request, user)  # Important to update the session
#             messages.success(request, 'Your password has been successfully changed.')
#             return redirect('warehouse_dashboard')
#         else:
#             messages.error(request, 'Please correct the error below.')
#     else:
#         form = ChangePasswordForm(request.user)
#     return render(request, 'warehouse/change_password.html', {'form': form})

def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to update the session
            messages.success(request, 'Your password has been successfully changed.')
            return redirect('warehouse_dashboard')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = ChangePasswordForm(request.user)
    return render(request, 'warehouse/change_password.html', {'form': form})


def confirm_arrival(request, package_id):
    if request.method == 'POST':
        package = Package.objects.get(pk=package_id)
        package.status = 'in_house'
        package.save()

        courier = package.courier
        if courier:
            courier.status = 'available'
            courier.save()
    
        sender_email = package.recipientEmail
        sender_message = f"Your package with ID {package.package_number} has arrived at the warehouse."
        send_mail('Package Arrival Notification', sender_message, 'garynkuraiji@gmail.com', [sender_email])

        # # Send email to warehouse
        # warehouse_email = 'warehouse@example.com'  # Replace with actual warehouse email
        # warehouse_message = f"A package with ID {package.package_number} has arrived at the warehouse."
        # send_mail('Package Arrival Notification', warehouse_message, 'sender@example.com', [warehouse_email])

        messages.success(request, "Package arrival notified successfully.")
    else:
        messages.error(request, "Invalid request.")

    return redirect('warehouse_dashboard')  # Replace with the appropriate URL for the warehouse dashboard

def ready_packages(request):
    ready_packages = Package.objects.filter(status__in=['warehouse_arrival', 'ready_for_pickup', 'in_house'])
    if request.method == 'POST':
        selected_packages = request.POST.getlist('selected_packages')
        courier_id = request.POST.get('courier')
        drop_pick_zone_id = request.POST.get('drop_pick_zone')

        if selected_packages and courier_id and drop_pick_zone_id:
            courier = get_object_or_404(User, id=courier_id, role='courier')
            drop_pick_zone = get_object_or_404(User, id=drop_pick_zone_id, role='drop_pick_zone')

            # Update the packages with the assigned courier and change their status
            packages = Package.objects.filter(id__in=selected_packages)
            packages.update(courier=courier, dropOffLocation=drop_pick_zone, status='ready_for_pickup')
            
            courier.status = 'on-trip'
            courier.save()

            messages.success(request, 'Packages successfully assigned to courier.')

            return redirect('ready_packages')
        
    context = {
        'ready_packages': ready_packages,
        'available_couriers': User.objects.filter(role='courier', status='available'),
        'available_drop_pick_zones': User.objects.filter(role='drop_pick_zone')
    }
    return render(request, 'warehouse/ready_packages.html', context)


def to_pickup(request, package_id):
    if request.method == 'POST':
        package = Package.objects.get(pk=package_id)
        package.status = 'in_transit'
        package.save()

    return redirect('ready_packages')  # Replace with the appropriate URL for the warehouse dashboard
