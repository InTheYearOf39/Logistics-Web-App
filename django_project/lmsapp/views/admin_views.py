from django.shortcuts import render, redirect, redirect, get_object_or_404
from django.db.models import Q, Case, When, IntegerField, Count
from lmsapp.utils import get_time_of_day
from lmsapp.models import Package, User
from lmsapp.utils import get_time_of_day
from django.shortcuts import redirect, get_object_or_404
from lmsapp.forms import WarehouseForm, DropPickForm
from django.contrib.auth.hashers import make_password



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

def users(request):
    users = User.objects.all()  # Retrieve all users from the database
    
    context = {
        'users': users
    }
    
    return render(request, 'admin/users.html', context)

def assign_courier(request, package_id):
    package = get_object_or_404(Package, id=package_id)

    if request.method == 'POST':
        courier_id = request.POST.get('courier')
        courier = get_object_or_404(User, id=courier_id, role='courier')

        previous_courier_status = courier.status  # Save the previous status

        package.courier = courier

        # Update the package status based on the delivery type
        if (package.deliveryType == 'premium' and package.status == 'upcoming') or (package.deliveryType == 'express' and package.status == 'upcoming'):
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


def riders(request):
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
    return render(request, 'admin/riders.html', context)

def admin_history(request):
    packages = Package.objects.filter(
        Q(status='completed')
    )
    context = {
        'packages': packages
    }
    return render(request, 'admin/admin_history.html', context)

def dropoffs(request):
    dropoff_locations = User.objects.filter(packages_dropped_off__status='dropped_off').distinct()
    packages_by_location = {}

    for dropoff_location in dropoff_locations:
        packages = Package.objects.filter(dropOffLocation=dropoff_location, status='dropped_off')
        packages_by_location[dropoff_location.name] = packages

    context = {
        'packages_by_location': packages_by_location,
    }
    return render(request, 'admin/dropoffs.html', context)





def dispatch(request):
    return render(request, 'admin/dispatch.html', {})

# def create_warehouse(request):
#     if request.method == 'POST':
#         form = WarehouseForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.role = 'warehouse'
#             # Set default password for the warehouse user
#             user.password = make_password('warehouse@warehouse')
#             form.save()
#             # Optionally, redirect to a success page
#             return redirect('warehouses')
#     else:
#         form = WarehouseForm()
#     return render(request, 'admin/create_warehouse.html', {'form': form})

def create_warehouse(request):
    if request.method == 'POST':
        form = WarehouseForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'warehouse'
            # Set default password for the warehouse user
            user.set_password('warehouse@warehouse')
            form.save()
            # Optionally, redirect to a success page
            return redirect('warehouses')
    else:
        form = WarehouseForm()
    return render(request, 'admin/create_warehouse.html', {'form': form})

def warehouses(request):
    warehouses = User.objects.filter(role='warehouse')
    context = {
        'warehouses': warehouses
    }
    return render(request, 'admin/warehouses.html', context)

# def create_drop_pick(request):
#     warehouses = User.objects.filter(role='warehouse')
#     if request.method == 'POST':
#         form = DropPickForm(request.POST)
#         if form.is_valid():
#             drop_pick = form.save(commit=False)
#             drop_pick.role = 'drop_pick_zone'
            
#             # Set default password for the drop_pick_zone user
#             drop_pick.password = make_password('droppick@droppick')
            
#             # Retrieve the selected warehouse ID from the form
#             warehouse_id = request.POST.get('warehouse')
#             if warehouse_id:
#                 warehouse = User.objects.get(id=warehouse_id)
#                 drop_pick.warehouse = warehouse

#             drop_pick.save()
#             return redirect('drop_pick_zones')
#     else:
#         form = DropPickForm()
    
#     return render(request, 'admin/create_drop_pick.html', {'form': form, 'warehouses': warehouses})

def create_drop_pick(request):
    warehouses = User.objects.filter(role='warehouse')
    if request.method == 'POST':
        form = DropPickForm(request.POST)
        if form.is_valid():
            drop_pick = form.save(commit=False)
            drop_pick.role = 'drop_pick_zone'
            
            # Set default password for the drop_pick_zone user
            drop_pick.set_password('droppick@droppick')
            
            # Retrieve the selected warehouse ID from the form
            warehouse_id = request.POST.get('warehouse')
            if warehouse_id:
                warehouse = User.objects.get(id=warehouse_id)
                drop_pick.warehouse = warehouse

            drop_pick.save()
            return redirect('drop_pick_zones')
    else:
        form = DropPickForm()
    
    return render(request, 'admin/create_drop_pick.html', {'form': form, 'warehouses': warehouses})



def drop_pick_zones(request):
    drop_pick_zones = User.objects.filter(role='drop_pick_zone')
    context = {
        'drop_pick_zones': drop_pick_zones
    }
    return render(request, 'admin/drop_pick_zones.html', context)