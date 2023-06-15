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
            courier = get_object_or_404(User, id=courier_id, role='courier')

            # Update the packages with the assigned courier and change their status
            packages = Package.objects.filter(id__in=selected_packages)
            packages.update(courier=courier, status='dispatched')

            messages.success(request, 'Packages successfully assigned to courier.')

            return redirect('warehouse_dashboard')

    context = {
        'packages_by_location': packages_by_location,
        'greeting_message': greeting_message,
        'available_couriers': User.objects.filter(role='courier')
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

    return render(request, 'warehouse/warehouse_dashboard.html', context)

