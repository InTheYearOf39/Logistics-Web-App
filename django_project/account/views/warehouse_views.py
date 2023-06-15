from django.shortcuts import render, redirect
from account.utils import get_time_of_day
from django.contrib.auth.decorators import login_required
from account.models import Package, User


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

    context = {
        'packages_by_location': packages_by_location,
        'greeting_message': greeting_message,
    }
    return render(request, 'warehouse/warehouse_dashboard.html', context)


