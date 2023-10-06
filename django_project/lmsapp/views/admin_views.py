import calendar

from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models import Q, Case, When, IntegerField, Count
from django.db.models.functions import ExtractDay, ExtractHour, ExtractMonth
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib import messages
from lmsapp.forms import CourierForm, WarehouseCreationForm, DropPickCreationForm, DropPickUserForm, WarehouseUserForm, EditWarehouseUserForm, EditDropPickUserForm, EditCourierForm
from lmsapp.models import Package, User, Warehouse, DropPickZone
from django.contrib.auth.hashers import make_password

from calendar import monthrange
from datetime import datetime, timedelta
import pandas as pd
from django.http import HttpResponse


def is_admin_user(user):
    return user.role == 'admin'

User = get_user_model()


@login_required
@user_passes_test(is_admin_user)
def admin_dashboard(request):  
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

    if total_packages_day != 0:
        percentage_delivered_day = (total_delivered_packages_day / total_packages_day) * 100
        percentage_delayed_day = (total_delayed_packages_day / total_packages_day) * 100
    else:
        percentage_delivered_day = 0
        percentage_delayed_day = 0
    # Calculate the average percentage of delivered and delayed packages for the week
    total_delivered_packages_week = sum(chart_data_week_completed)
    total_delayed_packages_week = sum(chart_data_week_ready_for_pickup)
    total_packages_week = total_delivered_packages_week + total_delayed_packages_week

    if total_packages_week != 0:
        percentage_delivered_week = (total_delivered_packages_week / total_packages_week) * 100
        percentage_delayed_week = (total_delayed_packages_week / total_packages_week) * 100
    else:
        percentage_delivered_week = 0
        percentage_delayed_week = 0

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
    return render(request, 'admin/admin_dashboard.html', context)

@login_required
@user_passes_test(is_admin_user)
def data_export(request):
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

    # Initialize arrays to hold the data for each day of the current week
    chart_data_week_completed = [0] * 7
    chart_data_week_ready_for_pickup = [0] * 7

    for total in weekly_totals:
        day = total['day'] - current_week_start.day  # Adjust the day to match array indices (start from 0)
        chart_data_week_completed[day] = total['total']
    
    for total in weekly_ready_for_pickup_totals:
        day = total['day'] - current_week_start.day  # Adjust the day to match array indices (start from 0)
        chart_data_week_ready_for_pickup[day] = total['total']

    excel_data = {
        'Total Packages': total_packages,
        'Day of the Week': ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        'Packages Delivered': chart_data_week_completed,
        'Packages Delayed': chart_data_week_ready_for_pickup
    }

    # Get the current date
    current_date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    # Create a Pandas DataFrame from the data
    df = pd.DataFrame(excel_data)

    # Create a response with the Excel file
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="Package_data_{current_date}.xlsx"'

    # Save the DataFrame to the Excel response
    df.to_excel(response, index=False, engine='openpyxl')

    return response

@login_required
@user_passes_test(is_admin_user)
def users(request):
    users = User.objects.filter(role='sender')  # Retrieve all senders from the database

    context = {
        'users': users
    }

    return render(request, 'admin/users.html', context)


"""
A function to query and display all couriers available on the system
"""

def couriers(request):
    couriers = User.objects.filter(role='courier')
    context = {
        'couriers': couriers,
        'success_message': request.GET.get("success_message", "")
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
A function to handle the creation of a warehouse through a form i.e 'WarehouseForm'. 
The form data is validated, and if valid, a warehouse is created, saved to the database.
If the request method is not POST or the form is not valid, the form is displayed to the user for input.
"""

# allow loading resources from other locations
@xframe_options_exempt
def create_warehouse(request):

    if request.method == 'POST':
        form = WarehouseCreationForm(request.POST)
        if form.is_valid():
            names = form.cleaned_data["name"].split()
            name = ' '.join([name.capitalize() for name in names])

            longitude = request.POST.get('longitude')
            latitude = request.POST.get('latitude')

            if not longitude or not latitude:
                address_error = "Something went wrong, re-enter the address."
                return render(request, 'admin/create_warehouse.html', {'form': form, 'address_error': address_error})
            
            tag = form.cleaned_data["tag"].upper()

            existing_warehouse = Warehouse.objects.filter(name=name).first()
            existing_warehouse_tag = Warehouse.objects.filter(tag=tag).first()
            existing_drop_pick_tag = DropPickZone.objects.filter(tag=tag).first()
            if existing_warehouse or existing_warehouse_tag or existing_drop_pick_tag:
                duplicate_error = "Warehouse name or tag already taken."
                return render(request, 'admin/create_warehouse.html', {'form': form, 'duplicate_error': duplicate_error})

            warehouse = form.save(commit=False)
            user = request.user

            address = form.cleaned_data["address"]
           
            warehouse.name = name
            warehouse.tag = tag
            warehouse.latitude = latitude
            warehouse.longitude = longitude
            warehouse.address = address
            warehouse.save(user=user)

            success_message = "You have successfully registered a warehouse!"
            return redirect(reverse('warehouses') + f'?success_message={success_message}')
        else:
            return render(request, 'admin/create_warehouse.html', {'form': form})
    else:
        form = WarehouseCreationForm(None)
    return render(request, 'admin/create_warehouse.html', {'form': form})


"""
A function to retrieve warehouses from the database by quering the db by the User model
for users with the 'warehouse' role and passing them to the 'admin/warehouses.html' template.
"""


def warehouses(request):
    warehouses = Warehouse.objects.all()
    warehouse_users = User.objects.filter(role='warehouse')
    context = {
        'success_message':request.GET.get("success_message", ""),
        'warehouses': warehouses,
        'warehouse_users': warehouse_users
    }
    return render(request, 'admin/warehouses.html', context)


"""
A function to handle the creation of a drop-pick zone through a form 'DropPickCreationForm'. 
The form data is validated, and if valid, a drop-pick zone is created, saved to the database.
The warehouses queryset is also passed to the template to display available warehouses for selection in the form.
Since a drop-pick zone must belong to a warehouse. If the request method is not POST or the form is not valid, 
the form is displayed to the user for input.
"""

# allow loading resources from other locations
@xframe_options_exempt
def create_drop_pick(request):
    if request.method == 'POST':
        form = DropPickCreationForm(request.POST)
        if form.is_valid():
            names = form.cleaned_data["name"].split()
            name = ' '.join([name.capitalize() for name in names])

            longitude = request.POST.get('longitude')
            latitude = request.POST.get('latitude')

            if not longitude or not latitude:
                address_error = "Something went wrong, re-enter the address."
                return render(request, 'admin/create_drop_pick.html', {'form': form, 'address_error': address_error})

            tag = form.cleaned_data["tag"].upper()

            existing_drop_pick = DropPickZone.objects.filter(name=name).first()
            existing_warehouse_tag = Warehouse.objects.filter(tag=tag).first()
            existing_drop_pick_tag = DropPickZone.objects.filter(tag=tag).first()

            if existing_drop_pick:
                duplicate_name = "Drop-pick name already taken! Please use another."
                return render(request, 'admin/create_drop_pick.html', {'form': form, 'duplicate_name': duplicate_name})
            
            if existing_warehouse_tag or existing_drop_pick_tag:
                duplicate_tag = "The Tag you chose is already in use! Please Choose another."
                return render(request, 'admin/create_drop_pick.html', {'form': form, 'duplicate_tag': duplicate_tag})

            user = request.user
            warehouse_id = form.cleaned_data['warehouse']
            address = form.cleaned_data["address"]

            drop_pick_zone = form.save(commit=False) 
            drop_pick_zone.name = name
            drop_pick_zone.tag = tag
            drop_pick_zone.warehouse = warehouse_id
            drop_pick_zone.latitude = latitude
            drop_pick_zone.longitude = longitude
            drop_pick_zone.address = address
            drop_pick_zone.save(user=user)

            success_message = "You have successfully registered a drop-pick zone!"
            return redirect(reverse('drop_pick_zones') + f'?success_message={success_message}')
        else:
            return render(request, 'admin/create_drop_pick.html', {'form': form})
    else:
        form = DropPickCreationForm(None)
        return render(request, 'admin/create_drop_pick.html', {'form': form})

def warehouse_users(request):
    warehouse_users = User.objects.filter(role='warehouse')
    context = {
        'warehouse_users': warehouse_users,
        'success_message': request.GET.get("success_message", "")
    }
    return render(request, 'admin/warehouse_users.html', context)


def drop_pick_users(request):
    drop_pick_users = User.objects.filter(role='drop_pick_zone')
    context = {
        'drop_pick_users': drop_pick_users,
        'success_message':request.GET.get("success_message", "")
    }
    return render(request, 'admin/drop_pick_users.html', context)


"""
A function to retrieve drop-pick zones from the database by querying the db by the User model
for users with the 'drop-pick' role and passing them to the 'admin/drop_pick_zones.html' template.
"""

def drop_pick_zones(request):
    drop_pick_zones = DropPickZone.objects.all()
    drop_pick_zone_users = User.objects.filter(role='drop_pick_zone')
    context = {
        'success_message':request.GET.get("success_message", ""),
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
            names = form.cleaned_data["name"].split()
            name = ' '.join([name.capitalize() for name in names])
            username = form.cleaned_data["username"]
            email = form.cleaned_data['email']
            phone = form.cleaned_data["phone"]
            warehouse_id = form.cleaned_data['warehouse']
            address = form.cleaned_data["address"]

            existing_username = User.objects.filter(username = username).first()
            existing_email = User.objects.filter(email = email).first()

            if existing_username:
                duplicate_username = "username already taken! Please choose another."
                return render(request, 'admin/create_courier.html', {'form': form, 'duplicate_username': duplicate_username})
            
            if existing_email:
                duplicate_email = "email already taken! Please choose another."
                return render(request, 'admin/create_courier.html', {'form': form, 'duplicate_email': duplicate_email})
            
            longitude = request.POST.get('longitude')
            latitude = request.POST.get('latitude')

            if not longitude or not latitude:
                address_error = "Something went wrong, re-enter the address."
                return render(request, 'admin/create_courier.html', {'form': form, 'address_error': address_error})

            courier = form.save(commit=False)
            courier.name = name
            courier.email = email
            courier.username = username
            courier.phone = phone
            courier.warehouse = warehouse_id
            courier.address = address
            courier.role = 'courier'
            courier.password = make_password('courier@courier')
            courier.longitude = longitude        
            courier.latitude = latitude        
            courier.created_by = request.user
            courier.save()

            success_message = f"You have successfully registered {courier.name}: as a courier assigned to {courier.warehouse} Warehouse!"
            return redirect(reverse('couriers') + f"?success_message={success_message}")
        else:
            return render(request, 'admin/create_courier.html', {'form': form})
    else:
        form = CourierForm(None)
    return render(request, 'admin/create_courier.html', {'form': form})

def create_warehouse_user(request):
    if request.method == 'POST':
        form = WarehouseUserForm(request.POST)
        if form.is_valid():
            names = form.cleaned_data["name"].split()
            name = ' '.join([name.capitalize() for name in names])
            username = form.cleaned_data["username"]
            email = form.cleaned_data['email']
            phone = form.cleaned_data["phone"]
            warehouse_id = form.cleaned_data['warehouse']

            existing_username = User.objects.filter(username = username).first()
            existing_email = User.objects.filter(email = email).first()

            if existing_username:
                duplicate_username = "username already taken! Please choose another."
                return render(request, 'admin/create_warehouse_user.html', {'form': form, 'duplicate_username': duplicate_username})
            
            if existing_email:
                duplicate_email = "email already taken! Please choose another."
                return render(request, 'admin/create_warehouse_user.html', {'form': form, 'duplicate_email': duplicate_email})

            user = form.save(commit=False)
            user.name = name
            user.email = email
            user.username = username
            user.phone = phone
            user.warehouse = warehouse_id
            user.role = 'warehouse'
            user.password = make_password('warehouse@warehouse')  
            user.created_by = request.user
            user.save()

            success_message = f"You have successfully registered {user.name}: as a warehouse administrator at {user.warehouse} Warehouse!"
            return redirect(reverse('warehouse_users') + f"?success_message={success_message}")
        else:
            return render(request, 'admin/create_warehouse_user.html', {'form': form})
    else:
        form = WarehouseUserForm(None)
    return render(request, 'admin/create_warehouse_user.html', {'form': form})


def create_drop_pick_user(request):
    if request.method == 'POST':
        form = DropPickUserForm(request.POST)
        if form.is_valid():
            names = form.cleaned_data["name"].split()
            name = ' '.join([name.capitalize() for name in names])
            username = form.cleaned_data["username"]
            email = form.cleaned_data['email']
            phone = form.cleaned_data["phone"]
            drop_pick_zone_id = form.cleaned_data['drop_pick_zone']

            existing_username = User.objects.filter(username = username).first()
            existing_email = User.objects.filter(email = email).first()

            if existing_username:
                duplicate_username = "username already taken! Please choose another."
                return render(request, 'admin/create_drop_pick_user.html', {'form': form, 'duplicate_username': duplicate_username})
            
            if existing_email:
                duplicate_email = "email already taken! Please choose another."
                return render(request, 'admin/create_drop_pick_user.html', {'form': form, 'duplicate_email': duplicate_email})

            user = form.save(commit=False)
            user.name = name
            user.email = email
            user.username = username
            user.phone = phone
            user.drop_pick_zone = drop_pick_zone_id
            user.role = 'drop_pick_zone'
            user.password = make_password('droppick@droppick')   
            user.created_by = request.user
            user.save()

            success_message = f"You have successfully registered {user.name}: as a drop-pick administrator at {user.drop_pick_zone} Drop-Pick zone!!"
            return redirect(reverse('drop_pick_users') + f"?success_message={success_message}")
        else:
            return render(request, 'admin/create_drop_pick_user.html', {'form': form})
    else:
        form = DropPickUserForm(None)
    return render(request, 'admin/create_drop_pick_user.html', {'form': form})

@xframe_options_exempt
def edit_warehouse(request, warehouse_id):
    obj = get_object_or_404(Warehouse, id=warehouse_id)

    if request.method == 'POST':
        form = WarehouseCreationForm(request.POST, instance=obj)
        if form.is_valid():
            names = form.cleaned_data["name"].split()
            name = ' '.join([name.capitalize() for name in names])

            longitude = request.POST.get('longitude')
            latitude = request.POST.get('latitude')

            if not longitude or not latitude:
                address_error = "Something went wrong, re-enter the address."
                return render(request, 'admin/edit_warehouse.html', {'form': form, 'address_error': address_error})
            
            tag = form.cleaned_data["tag"].upper()

             # Exclude the current warehouse from the queries
            existing_warehouse = Warehouse.objects.filter(~Q(id=warehouse_id), name=name).first()
            existing_warehouse_tag = Warehouse.objects.filter(~Q(id=warehouse_id), tag=tag).first()
            existing_drop_pick_tag = DropPickZone.objects.filter(tag=tag).first()
            
            duplicate_name_error = None
            duplicate_tag_error = None


            if existing_warehouse: 
                duplicate_name_error = "Warehouse name already taken! Please use another."
            
            if existing_warehouse_tag or existing_drop_pick_tag:
                duplicate_tag_error = "The Tag you chose is already in use! Please Choose another."
                return render(request, 'admin/edit_warehouse.html', {'form': form, 'duplicate_tag_error': duplicate_tag_error, 'duplicate_name_error': duplicate_name_error})

        
            address = form.cleaned_data["address"]

            warehouse = Warehouse.objects.get(id=warehouse_id)
            warehouse.name = name
            warehouse.tag = tag
            warehouse.latitude = latitude
            warehouse.longitude = longitude
            warehouse.address = address
            warehouse.modified_by = request.user
            warehouse.save()

            success_message = f"You have successfully updated {warehouse.name} warehouse's details!"
            return redirect(reverse('warehouses') + f'?success_message={success_message}')
            
        else:
            return render(request, 'admin/edit_warehouse.html', {'form': form})
    else:
        form = WarehouseCreationForm(instance = obj)
        return render(request, 'admin/edit_warehouse.html', {'form': form})

@xframe_options_exempt
def edit_drop_pick_zone(request, drop_pick_zone_id):
    obj = get_object_or_404(DropPickZone, id=drop_pick_zone_id)
    
    if request.method == 'POST':
        form = DropPickCreationForm(request.POST, instance=obj)
        if form.is_valid():
            names = form.cleaned_data["name"].split()
            name = ' '.join([name.capitalize() for name in names])

            longitude = request.POST.get('longitude')
            latitude = request.POST.get('latitude')

            if not longitude or not latitude:
                address_error = "Something went wrong, re-enter the address."
                return render(request, 'admin/create_drop_pick.html', {'form': form, 'address_error': address_error})

            tag = form.cleaned_data["tag"].upper()

            existing_drop_pick = DropPickZone.objects.filter(~Q(id=drop_pick_zone_id),name=name).first()
            existing_warehouse_tag = Warehouse.objects.filter(tag=tag).first()
            existing_drop_pick_tag = DropPickZone.objects.filter(~Q(id=drop_pick_zone_id),tag=tag).first()

            duplicate_name_error = None
            duplicate_tag_error = None

            if existing_drop_pick: 
                duplicate_name_error = "Drop-pick name already taken! Please use another."
            
            if existing_warehouse_tag or existing_drop_pick_tag:
                duplicate_tag_error = "The Tag you chose is already in use! Please Choose another."
                return render(request, 'admin/edit_drop_pick_zone.html', {'form': form, 'duplicate_tag_error': duplicate_tag_error, 'duplicate_name_error': duplicate_name_error})

            warehouse_id = form.cleaned_data['warehouse']
            address = form.cleaned_data["address"]

            drop_pick_zone = DropPickZone.objects.get(id=drop_pick_zone_id) 
            drop_pick_zone.name = name
            drop_pick_zone.tag = tag
            drop_pick_zone.warehouse = warehouse_id
            drop_pick_zone.latitude = latitude
            drop_pick_zone.longitude = longitude
            drop_pick_zone.address = address
            drop_pick_zone.modified_by = request.user
            drop_pick_zone.save()

            success_message = f"You have successfully updated {drop_pick_zone.name} drop-pick zone's details!"
            return redirect(reverse('drop_pick_zones') + f'?success_message={success_message}')
        else:
            return render(request, 'admin/edit_drop_pick_zone.html', {'form': form})
    else:
        form = DropPickCreationForm(instance=obj)
        return render(request, 'admin/edit_drop_pick_zone.html', {'form': form})
    
def edit_drop_pick_zone_user(request, drop_pick_zone_user_id):
    obj = get_object_or_404(User, id=drop_pick_zone_user_id)

    if request.method == 'POST':
        form = EditDropPickUserForm(request.POST, instance=obj) 
        if form.is_valid():

            phone = form.cleaned_data["phone"]
            drop_pick_zone_id = form.cleaned_data['drop_pick_zone']

            user = User.objects.get(id=drop_pick_zone_user_id) 
            user.phone = phone
            user.drop_pick_zone = drop_pick_zone_id  
            user.modified_by = request.user
            user.save()

            success_message = f"You have successfully updated {user.name}'s details"
            return redirect(reverse('drop_pick_users') + f"?success_message={success_message}")
        else:
            return render(request, 'admin/edit_drop_pick_zone_user.html', {'form': form})
    else:
        form = EditDropPickUserForm(instance=obj)
        return render(request, 'admin/edit_drop_pick_zone_user.html', {'form': form })
    
def edit_warehouse_user(request, user_id):
    obj = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = EditWarehouseUserForm(request.POST, instance=obj)
        if form.is_valid():        

            phone = form.cleaned_data["phone"]
            warehouse_id = form.cleaned_data['warehouse']

            user = User.objects.get(id=user_id) 
            user.phone = phone
            user.warehouse = warehouse_id  
            user.modified_by = request.user
            user.save()

            success_message = f"You have successfully updated {user.name}'s details"
            return redirect(reverse('warehouse_users') + f"?success_message={success_message}")
        else:
            return render(request, 'admin/edit_warehouse_user.html', {'form': form})
    else:
        form = EditWarehouseUserForm(instance = obj)
        return render(request, 'admin/edit_warehouse_user.html', {'form': form })

def edit_courier(request, courier_id):
    obj = get_object_or_404(User, id=courier_id)

    if request.method == 'POST':
        form = EditCourierForm(request.POST, instance = obj)
        if form.is_valid():
            phone = form.cleaned_data["phone"]
            warehouse_id = form.cleaned_data['warehouse']
            address = form.cleaned_data["address"]
            longitude = request.POST.get('longitude')
            latitude = request.POST.get('latitude')

            if not longitude or not latitude:
                address_error = "Something went wrong, re-enter the address."
                return render(request, 'admin/edit_courier.html', {'form': form, 'address_error': address_error})

            courier = User.objects.get(id=courier_id)
            courier.phone = phone
            courier.warehouse = warehouse_id
            courier.address = address
            courier.longitude = longitude        
            courier.latitude = latitude        
            courier.modified_by = request.user
            courier.save()

            success_message = f"You have successfully updated {courier.name}'s details"
            return redirect(reverse('couriers') + f"?success_message={success_message}")
        else:
            return render(request, 'admin/edit_courier.html', {'form': form})
    else:
        form = EditCourierForm(instance = obj)
        return render(request, 'admin/edit_courier.html', {'form': form})

def delete_courier(request, courier_id):
    courier = get_object_or_404(User, id=courier_id, role='courier')

    if request.method == 'POST':
        courier.delete()
        return redirect('couriers')

    return redirect('couriers')

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

def delete_warehouse_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        # Delete the warehouse user
        user.delete()
        return redirect('warehouse_users')

    # If the request method is not POST, show the confirmation modal
    return render(request, 'admin/delete_warehouse_user.html', {'user': user})

def delete_warehouse(request, warehouse_id):
    warehouse = get_object_or_404(Warehouse, id=warehouse_id)

    if request.method == 'POST':
        # Delete the warehouse
        warehouse.delete()
        return redirect('warehouses')

    return render(request, 'admin/warehouses.html', {'warehouse': warehouse})

def delete_drop_pick_zone(request, drop_pick_zone_id):
    drop_pick_zone = get_object_or_404(DropPickZone, id=drop_pick_zone_id)
    if request.method == 'POST':
        # Perform the delete operation
        drop_pick_zone.delete()
        return redirect('drop_pick_zones')

    return render(request, 'admin/delete_drop_pick_zone.html', {'drop_pick_zone': drop_pick_zone})


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
