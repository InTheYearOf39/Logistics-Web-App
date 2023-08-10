import calendar

from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models import Q, Case, When, IntegerField, Count
from django.db.models.functions import ExtractDay, ExtractHour, ExtractMonth
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.clickjacking import xframe_options_exempt

from lmsapp.forms import CourierForm
from lmsapp.models import Package, User, Warehouse, DropPickZone
from lmsapp.utils import get_time_of_day

from calendar import monthrange
from datetime import datetime, timedelta

User = get_user_model()

""" 
A function to handle the logic for an admin dashboard page, including querying and
displaying packages and functionality depending on the different delivery types, 
and rendering the corresponding template with the appropriate context
"""


def admin(request):
    packages = Package.objects.filter(
        Q(status='ongoing') | Q(status='dropped_off') | Q(status='ready_for_pickup') | Q(status='upcoming')
    ).order_by(
        Case(
            When(status='upcoming', then=0),
            When(status='dropped_off', then=1),
            When(status='ongoing', then=2),
            default=3,
            output_field=IntegerField()
        ),
        '-assigned_at'  # Sort by assignment day in descending order
    )

    greeting_message = get_time_of_day()

    if request.method == 'POST':
        package_id = request.POST.get('package_id')
        delivery_type = request.POST.get('delivery_type')

        # Check the delivery type of the package
        if delivery_type == 'standard':
            package = get_object_or_404(Package, id=package_id, status='dropped_off')
            return redirect('assign_courier', package_id=package.id)
        elif delivery_type == 'premium' or delivery_type == 'express':
            package = get_object_or_404(Package, id=package_id, status='upcoming')
            return redirect('assign_courier', package_id=package.id)

    context = {
        'greeting_message': greeting_message,
        'packages': packages
    }
    return render(request, 'admin/admin_dashboard.html', context)

def master_dashboard(request):  
    total_packages = Package.objects.all().count()      
    # Get the datetime for the start of the current week
    current_week_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=timezone.now().weekday())
    current_week_end = current_week_start + timedelta(days=7)
    
    weekly_totals = Package.objects.filter(
        status__in=['completed'],
        completed_at__range=(current_week_start, current_week_end)
    ).annotate(day=ExtractDay('completed_at')).values('day').annotate(total=Count('id')).order_by('day')
    
    weekly_ready_for_pickup_totals = Package.objects.filter(
        status='ready_for_pickup',
        received_at__range=(current_week_start, current_week_end)
    ).annotate(day=ExtractDay('received_at')).values('day').annotate(total=Count('id')).order_by('day')

    # Initialize an array to hold the data for each day of the current week
    chart_data_week_completed = [0] * 7
    chart_data_week_ready_for_pickup = [0] * 7

    for total in weekly_totals:
        day = total['day'] - current_week_start.day  # Adjust the day to match array indices (start from 0)
        chart_data_week_completed[day] = total['total']
    
    for total in weekly_ready_for_pickup_totals:
        day = total['day'] - current_week_start.day  # Adjust the day to match array indices (start from 0)
        chart_data_week_ready_for_pickup[day] = total['total']

    # Generate the labels for the weekly chart
    start_day_label = current_week_start.strftime('%B %d, %Y')
    end_day_label = current_week_end.strftime('%B %d, %Y')
    week_label = f"{start_day_label} to {end_day_label}"
    
    total_delivered_packages_day = sum(chart_data_week_completed)
    total_delayed_packages_day = sum(chart_data_week_ready_for_pickup)
    total_packages_day = total_delivered_packages_day + total_delayed_packages_day

    percentage_delivered_day = (total_delivered_packages_day / total_packages_day) * 100
    percentage_delayed_day = (total_delayed_packages_day / total_packages_day) * 100

    # Calculate the average percentage of delivered and delayed packages for the week
    total_delivered_packages_week = sum(chart_data_week_completed)
    total_delayed_packages_week = sum(chart_data_week_ready_for_pickup)
    total_packages_week = total_delivered_packages_week + total_delayed_packages_week

    percentage_delivered_week = (total_delivered_packages_week / total_packages_week) * 100
    percentage_delayed_week = (total_delayed_packages_week / total_packages_week) * 100

    context = {
        # Your existing context data
        'total_packages': total_packages,
        'percentage_delivered_day': percentage_delivered_day,
        'percentage_delayed_day': percentage_delayed_day,
        'percentage_delivered_week': percentage_delivered_week,
        'percentage_delayed_week': percentage_delayed_week,
        'week_label': week_label,
        'chart_data_week_packages': {
            "chart_type": "bar",
            "x_values": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            "datasets": [
                {
                    "label": "packages delivered",
                    "data": chart_data_week_completed,  # Use the dynamic data here
                    "backgroundColor": 'orange',
                    "borderColor": 'orange',
                    "borderWidth": 1,
                },
                {
                    "label": "packages delayed",
                    "data": chart_data_week_ready_for_pickup,  # Use the dynamic data here
                    "backgroundColor": 'green',
                    "borderColor": 'green',
                    "borderWidth": 1,
                }
            ],
            "chart_title": f'Packages Per Day in {current_week_start.strftime("%B %d, %Y")} to {current_week_end.strftime("%B %d, %Y")}',
            "x_title": 'Day of the Week',
            "y_title": 'Packages'
        }
    }
    return render(request, 'admin/master_dashboard.html', context)

def users(request):
    users = User.objects.all()  # Retrieve all users from the database

    context = {
        'users': users
    }

    return render(request, 'admin/users.html', context)


"""
 A function to handle the assignment of a courier to a package. It retrieves the package and couriers, 
 updates the package and courier objects, and redirects to the admin dashboard after a successful assignment.
 """


def assign_courier(request, package_id):
    package = get_object_or_404(Package, id=package_id)

    if request.method == 'POST':
        courier_id = request.POST.get('courier')
        courier = get_object_or_404(User, id=courier_id, role='courier')

        previous_courier_status = courier.status  # Save the previous status

        package.courier = courier

        # Update the package status based on the delivery type
        if (package.deliveryType == 'premium' and package.status == 'upcoming') or (
                package.deliveryType == 'express' and package.status == 'upcoming'):
            package.status = 'ongoing'
        # elif package.deliveryType == 'premium' and package.status == 'upcoming':
        #     package.status = 'ongoing'

        package.save()

        # Update the courier status to "on-trip" only if they were not already on-trip
        if previous_courier_status != 'on-trip' and package.status == 'ongoing':
            courier.status = 'on-trip'
            courier.save()

        return redirect('admin_dashboard')

    couriers = User.objects.filter(role='courier', status='available')  # Filter couriers by status='available'
    context = {
        'package_id': package_id,
        'couriers': couriers
    }

    return render(request, 'admin/assign_courier.html', context)


"""
A function to update the status of couriers based on the status of their assigned packages. If a courier has assigned packages,
 their status is determined by the presence of 'ongoing' or 'arrived' packages. If a courier has no assigned packages, 
 their status is set to 'available'. The updated courier objects are saved in the database, and the 'admin/couriers.html' 
 template is rendered with the couriers queryset as context.
"""


def couriers(request):
    couriers = User.objects.filter(role='courier')

    for courier in couriers:
        assigned_packages = courier.assigned_packages.all()

        if assigned_packages.exists():

            if assigned_packages.filter(status__in=['ongoing', 'arrived']).exists():
                courier.status = 'on-trip'
            else:
                courier.status = 'available'
        else:
            courier.status = 'available'

        courier.save()

    context = {
        'couriers': couriers
    }
    return render(request, 'admin/couriers.html', context)


def admin_history(request):
    packages = Package.objects.filter(
        Q(status='completed')
    )
    context = {
        'packages': packages
    }
    return render(request, 'admin/admin_history.html', context)


"""
A Function to retrieve dropped off items and group the packages by their respective drop-off locations and
render them on the 'admin/dropoffs.html' template.
 """


# def dropoffs(request):
#     dropoff_locations = DropPickZone.objects.filter(packages_dropped_off__status='dropped_off').distinct()
#     packages_by_location = {}

#     for dropoff_location in dropoff_locations:
#         packages = Package.objects.filter(dropOffLocation=dropoff_location, status='dropped_off')
#         packages_by_location[dropoff_location.name] = packages

#     context = {
#         'packages_by_location': packages_by_location,
#     }
#     return render(request, 'admin/dropoffs.html', context)

# def dropoffs(request):
#     packages = Package.objects.filter(status='dropped_off')

#     context = {
#         'packages': packages,
#     }
#     return render(request, 'admin/dropoffs.html', context)

def dropoffs(request):
    packages = Package.objects.filter(status='dropped_off').select_related('dropOffLocation')
    sorted_packages = sorted(packages, key=lambda package: package.dropOffLocation.tag)

    context = {
        'packages': sorted_packages,
    }
    return render(request, 'admin/dropoffs.html', context)


def dispatch(request):
    return render(request, 'admin/dispatch.html', {})


"""
A function to handle the creation of a warehouse through a form i.e 'WarehouseForm'. 
The form data is validated, and if valid, a warehouse is created, saved to the database.
If the request method is not POST or the form is not valid, the form is displayed to the user for input.
"""


# allow loading resources from other locations
@xframe_options_exempt
def create_warehouse(request):
    if request.method == 'POST':
        user=request.user

        name = request.POST.get('name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        tag = request.POST.get('tag')
        longitude = request.POST.get('longitude')
        latitude = request.POST.get('latitude')

        warehouse = Warehouse(name=name, address=address, phone=phone, tag=tag, latitude=latitude, longitude=longitude)
        # warehouse.created_by = user
        warehouse.save(user=user)

        return redirect('warehouses')

    return render(request, 'admin/create_warehouse.html')


"""
A function to retrieve warehouses from the database by quering the db by the User model
for users with the 'warehouse' role and passing them to the 'admin/warehouses.html' template.
"""


def warehouses(request):
    warehouses = Warehouse.objects.all()
    warehouse_users = User.objects.filter(role='warehouse')
    context = {
        'warehouses': warehouses,
        'warehouse_users': warehouse_users
    }
    return render(request, 'admin/warehouses.html', context)


"""
A function to handle the creation of a drop-pick zone user through a form 'DropPickForm'. 
The form data is validated, and if valid, a drop-pick zone is created, saved to the database.
The warehouses queryset is also passed to the template to display available warehouses for selection in the form.
Since a drop-pick zone must belong to a warehouse. If the request method is not POST or the form is not valid, 
the form is displayed to the user for input.
"""


# allow loading resources from other locations
@xframe_options_exempt
def create_drop_pick(request):
    if request.method == 'POST':
        user=request.user
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        tag = request.POST.get('tag')
        warehouse_id = request.POST.get('warehouse')
        longitude = request.POST.get('longitude')
        latitude = request.POST.get('latitude')

        warehouse = Warehouse.objects.get(id=warehouse_id)

        drop_pick_zone = DropPickZone(name=name, address=address, phone=phone, tag=tag, warehouse=warehouse,
                                      longitude=longitude, latitude=latitude)
        drop_pick_zone.save(user=user)

        return redirect('drop_pick_zones')

    warehouses = Warehouse.objects.all()
    context = {
        'warehouses': warehouses
    }
    return render(request, 'admin/create_drop_pick.html', context)


"""
A function to retrieve drop-pick zones from the database by querying the db by the User model
for users with the 'drop-pick' role and passing them to the 'admin/drop_pick_zones.html' template.
"""


def drop_pick_zones(request):
    drop_pick_zones = DropPickZone.objects.all()
    drop_pick_zone_users = User.objects.filter(role='drop_pick_zone')
    context = {
        'drop_pick_zones': drop_pick_zones,
        'drop_pick_zone_users': drop_pick_zone_users
    }
    return render(request, 'admin/drop_pick_zones.html', context)


"""
A function to handle the creation of a courier user through a form 'CourierForm'. 
The form data is validated, and if valid, a courier user is created, saved to the database
and the user is redirected to the 'admin/couriers.html' page. If the request method is not POST 
or the form is not valid, the form is displayed to the user for input.
"""


def create_courier(request):
    if request.method == 'POST':
        form = CourierForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'courier'
            # Set default password for the courier user
            user.set_password('courier@courier')

            # Get the latitude and longitude from the form data
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            user.latitude = latitude
            user.longitude = longitude
            user.created_by = request.user

            form.save()
            # Optionally, redirect to a success page
            return redirect('couriers')
    else:
        form = CourierForm()
    return render(request, 'admin/create_courier.html', {'form': form})


def create_warehouse_user(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('username')
        warehouse_id = request.POST.get('warehouse')

        if warehouse_id:
            warehouse = get_object_or_404(Warehouse, id=warehouse_id)

            # Create the user with the role "warehouse"
            user = User.objects.create_user(username=username, password='warehouse@warehouse', role='warehouse',
                                            name=name, warehouse=warehouse)
            user.created_by = request.user
            user.save()

            return redirect('warehouse_users')

    # Retrieve the warehouses
    warehouses = Warehouse.objects.all()

    context = {
        'warehouses': warehouses
    }
    return render(request, 'admin/create_warehouse_user.html', context)


def create_drop_pick_user(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('username')
        drop_pick_zone_id = request.POST.get('drop_pick_zone')

        if drop_pick_zone_id:
            drop_pick_zone = get_object_or_404(DropPickZone, id=drop_pick_zone_id)

            # Create the user with the role "drop_pick_zone"
            user = User.objects.create_user(username=username, password='droppick@droppick', role='drop_pick_zone',
                                            name=name, drop_pick_zone=drop_pick_zone)
            
            user.created_by = request.user
            user.save()

            return redirect('drop_pick_users')

    # Retrieve the drop pick zones
    drop_pick_zones = DropPickZone.objects.all()

    context = {
        'drop_pick_zones': drop_pick_zones
    }
    return render(request, 'admin/create_drop_pick_user.html', context)


# views.py
def edit_warehouse(request, warehouse_id):
    warehouse = get_object_or_404(Warehouse, id=warehouse_id)

    if request.method == 'POST':
        user = request.user
        # Get the form data from the request.POST dictionary
        name = request.POST['name']
        address = request.POST['address']
        phone = request.POST['phone']
        tag = request.POST['tag']
        latitude = request.POST['latitude']
        longitude = request.POST['longitude']

        # Update the warehouse model instance with the new data
        warehouse.name = name
        warehouse.address = address
        warehouse.phone = phone
        warehouse.tag = tag
        warehouse.latitude = latitude
        warehouse.longitude = longitude

        # Save the updated warehouse details to the database
        warehouse.save(user=user)

        # Redirect to the warehouses list page after editing
        return redirect('warehouses')

    return render(request, 'admin/edit_warehouse.html', {'warehouse': warehouse})


def delete_warehouse(request, warehouse_id):
    warehouse = get_object_or_404(Warehouse, id=warehouse_id)

    if request.method == 'POST':
        # Delete the warehouse
        warehouse.delete()
        return redirect('warehouses')

    return render(request, 'admin/warehouses.html', {'warehouse': warehouse})


def edit_warehouse_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        # Check if the form was submitted for deletion
        if 'delete_user' in request.POST:
            # Delete the warehouse user
            user.delete()
            return redirect('warehouse_users_list')

        # If not deletion, handle the form for updating the user details
        name = request.POST.get('name')
        username = request.POST.get('username')
        warehouse_id = request.POST.get('warehouse')

        if warehouse_id:
            warehouse = get_object_or_404(Warehouse, id=warehouse_id)

            # Update the user details
            user.name = name
            user.username = username
            user.warehouse = warehouse
            user.modified_by = request.user
            user.save()

            return redirect('warehouse_users')

    # Retrieve the warehouses
    warehouses = Warehouse.objects.all()

    context = {
        'user': user,
        'warehouses': warehouses
    }
    return render(request, 'admin/edit_warehouse_user.html', context)


def delete_warehouse_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        # Delete the warehouse user
        user.delete()
        return redirect('warehouse_users')

    # If the request method is not POST, show the confirmation modal
    return render(request, 'admin/delete_warehouse_user.html', {'user': user})


def edit_drop_pick_zones(request, drop_pick_zone_id):
    drop_pick_zone = get_object_or_404(DropPickZone, id=drop_pick_zone_id)

    if request.method == 'POST':
        # Get form data
        user = request.user
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        tag = request.POST.get('tag')
        warehouse_id = request.POST.get('warehouse')

        if warehouse_id:
            warehouse = get_object_or_404(Warehouse, id=warehouse_id)

            # Update the drop-pick zone details
            drop_pick_zone.name = name
            drop_pick_zone.address = address
            drop_pick_zone.phone = phone
            drop_pick_zone.tag = tag
            drop_pick_zone.warehouse = warehouse
            drop_pick_zone.save(user=user)

            return redirect('drop_pick_zones')

    # Retrieve the warehouses
    warehouses = Warehouse.objects.all()

    context = {
        'drop_pick_zone': drop_pick_zone,
        'warehouses': warehouses,
    }
    return render(request, 'admin/edit_drop_pick_zones.html', context)


def delete_drop_pick_zone(request, drop_pick_zone_id):
    drop_pick_zone = get_object_or_404(DropPickZone, id=drop_pick_zone_id)
    if request.method == 'POST':
        # Perform the delete operation
        drop_pick_zone.delete()
        return redirect('drop_pick_zones')

    return render(request, 'admin/delete_drop_pick_zone.html', {'drop_pick_zone': drop_pick_zone})


def edit_drop_pick_zone_user(request, drop_pick_zone_user_id):
    drop_pick_zone_user = get_object_or_404(User, id=drop_pick_zone_user_id, role='drop_pick_zone')

    if request.method == 'POST':
        if 'delete' in request.POST:
            # Delete the drop-pick zone user
            drop_pick_zone_user.delete()
            return redirect('drop_pick_users')

        # If 'delete' was not in the request.POST, it means we're updating the user details
        # Get form data
        name = request.POST.get('name')
        username = request.POST.get('username')
        drop_pick_zone_id = request.POST.get('drop_pick_zone')

        if drop_pick_zone_id:
            drop_pick_zone = get_object_or_404(DropPickZone, id=drop_pick_zone_id)

            # Update the drop-pick zone user details
            drop_pick_zone_user.name = name
            drop_pick_zone_user.username = username
            drop_pick_zone_user.drop_pick_zone = drop_pick_zone
            drop_pick_zone_user.modified_by = request.user
            drop_pick_zone_user.save()

            return redirect('drop_pick_users')

    # Retrieve the drop pick zones
    drop_pick_zones = DropPickZone.objects.all()

    context = {
        'drop_pick_zone_user': drop_pick_zone_user,
        'drop_pick_zones': drop_pick_zones,
    }
    return render(request, 'admin/edit_drop_pick_zone_user.html', context)


def delete_drop_pick_zone_user(request, drop_pick_zone_user_id):
    drop_pick_zone_user = get_object_or_404(User, id=drop_pick_zone_user_id, role='drop_pick_zone')

    if request.method == 'POST':
        # Delete the drop-pick zone user
        drop_pick_zone_user.delete()
        return redirect('drop_pick_users')

    # Since there's no separate template, we don't need to render anything here.
    # The confirmation modal will handle the user's decision.

    # You can also add extra context here if required.

    return redirect('drop_pick_users')  # Redirect back to the drop_pick_zones page.


def warehouse_users(request):
    warehouse_users = User.objects.filter(role='warehouse')
    context = {
        'warehouse_users': warehouse_users
    }
    return render(request, 'admin/warehouse_users.html', context)


def drop_pick_users(request):
    drop_pick_users = User.objects.filter(role='drop_pick_zone')
    context = {
        'drop_pick_users': drop_pick_users
    }
    return render(request, 'admin/drop_pick_users.html', context)


def edit_courier(request, courier_id):
    courier = get_object_or_404(User, id=courier_id, role='courier')

    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        username = request.POST.get('username')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        # Update the courier details
        courier.name = name
        courier.username = username
        courier.phone = phone
        courier.address = address
        courier.modified_by = request.user
        courier.save()

        return redirect('couriers')

    context = {
        'courier': courier,
    }
    return render(request, 'admin/edit_courier.html', context)


def delete_courier(request, courier_id):
    courier = get_object_or_404(User, id=courier_id, role='courier')

    if request.method == 'POST':
        courier.delete()
        return redirect('couriers')

    return redirect('couriers')


def package_reports(request):
    delivered_packages = Package.objects.filter(status='completed')
    ready_packages = Package.objects.filter(status='ready_for_pickup')
    # Get the datetime for the start of the current day
    current_day_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)

    hourly_totals = Package.objects.filter(
        status__in=['ready_for_pickup'],
        received_at__gte=current_day_start
    ).annotate(hour=ExtractHour('received_at')).values('hour').annotate(total=Count('id')).order_by('hour')

    # Initialize an array to hold the data for each hour of the day
    chart_data = [0] * 24

    for total in hourly_totals:
        hour = total['hour']
        chart_data[hour] = total['total']

    # Get the number of days in the current month
    current_month = timezone.now().month
    days_in_month = calendar.monthrange(timezone.now().year, current_month)[1]

    # Get the datetime for the start of the current month
    current_month_start = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    daily_totals = Package.objects.filter(
        status__in=['completed'],
        completed_at__gte=current_month_start
    ).annotate(day=ExtractDay('completed_at')).values('day').annotate(total=Count('id')).order_by('day')

    # Initialize an array to hold the data for each day of the month
    chart_data_month = [0] * days_in_month

    for total in daily_totals:
        day = total['day'] - 1  # Adjust the day to match array indices (start from 0)
        chart_data_month[day] = total['total']

    # Get the datetime for the start of the current year
    current_year_start = timezone.now().replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)

    monthly_totals = Package.objects.filter(
        status__in=['completed'],
        completed_at__gte=current_year_start
    ).annotate(month=ExtractMonth('completed_at')).values('month').annotate(total=Count('id')).order_by('month')

    # Initialize an array to hold the data for each month of the year
    chart_data_year = [0] * 12

    for total in monthly_totals:
        month = total['month'] - 1  # Adjust the month to match array indices (start from 0)
        chart_data_year[month] = total['total']

    # Get the year for the current year
    current_year = timezone.now().year
    month_name = current_month_start.strftime('%B')

    context = {
        'delivered_packages': delivered_packages,
        'ready_packages': ready_packages,
        'month_name': month_name,
        'current_year': current_year,
        'chart_data_packages': {
            "chart_type": "bar",
            "x_values": list(range(24)),  # Hours of the day (0 to 23)
            "datasets": [
                {
                    "label": "packages received per hour",
                    "data": chart_data,  # Use the dynamic data here
                    "backgroundColor": 'red',
                    "borderColor": 'red',
                    "borderWidth": 1,
                }
            ],
            "chart_title": 'Packages Per Hour',
            "x_title": 'Hour of the Day',
            "y_title": 'Packages'
        },
        'chart_data_month_packages': {
            "chart_type": "bar",
            "x_values": [day for day in range(1, days_in_month + 1)],  # Days of the month (1 to last day)
            "datasets": [
                {
                    "label": f"packages delivered in {month_name}",
                    "data": chart_data_month,  # Use the dynamic data here
                    "backgroundColor": 'blue',
                    "borderColor": 'blue',
                    "borderWidth": 1,
                }
            ],
            "chart_title": f"Packages Per Day in {current_month}",
            "x_title": 'Day of the Month',
            "y_title": 'Packages'
        },
        'chart_data_year_packages': {
            "chart_type": "bar",
            "x_values": [month for month in range(1, 13)],  # Months of the year (1 to 12)
            "datasets": [
                {
                    "label": f"packages delivered in {current_year}",
                    "data": chart_data_year,  # Use the dynamic data here
                    "backgroundColor": 'green',
                    "borderColor": 'green',
                    "borderWidth": 1,
                }
            ],
            "chart_title": f'Packages Per Month in {current_year}',
            "x_title": 'Month of the Year',
            "y_title": 'Packages'
        }
    }

    return render(request, 'admin/package_reports.html', context)

def user_reports(request):
    user_list = User.objects.filter(role__in=['courier', 'warehouse', 'drop_pick_zone'])

    context = {
        'user_list': user_list,
    }
        
    return render(request, 'admin/user_reports.html', context)
