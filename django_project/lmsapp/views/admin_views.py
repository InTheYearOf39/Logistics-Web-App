from django.shortcuts import render, redirect, redirect, get_object_or_404
from django.db.models import Q, Case, When, IntegerField, Count
from lmsapp.utils import get_time_of_day
from lmsapp.models import Package, User
from lmsapp.utils import get_time_of_day
from django.shortcuts import redirect, get_object_or_404
from lmsapp.forms import WarehouseForm, DropPickForm
from django.contrib.auth.hashers import make_password
from lmsapp.forms import CourierForm


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

# A function to retrieve all the users from the database, and send the user information to a template 
def users(request):
    users = User.objects.all()
    
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

"""
A function to update the status of couriers based on the status of their assigned packages. If a courier has assigned packages,
 their status is determined by the presence of 'ongoing' or 'arrived' packages. If a courier has no assigned packages, 
 their status is set to 'available'. The updated courier objects are saved in the database, and the 'admin/riders.html' 
 template is rendered with the couriers queryset as context.
"""
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


# A function to to retrieve packages with the status 'completed' and pass them to the 'admin/admin_history.html' template
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

"""
A function to handle the creation of a warehouse through a form i.e 'WarehouseForm'. 
The form data is validated, and if valid, a warehouse is created, saved to the database.
If the request method is not POST or the form is not valid, the form is displayed to the user for input.
"""
def create_warehouse(request):
    if request.method == 'POST':
        form = WarehouseForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'warehouse'
            # Set default password for the warehouse user
            user.set_password('warehouse@warehouse')
            form.save()

            return redirect('warehouses')
    else:
        form = WarehouseForm()
    return render(request, 'admin/create_warehouse.html', {'form': form})

"""
A function to retrieve warehouses from the database by quering the db by the User model
for users with the 'warehouse' role and passing them to the 'admin/warehouses.html' template.
"""
def warehouses(request):
    warehouses = User.objects.filter(role='warehouse')
    context = {
        'warehouses': warehouses
    }
    return render(request, 'admin/warehouses.html', context)

"""
A function to handle the creation of a drop-pick zone user through a form 'DropPickForm'. 
The form data is validated, and if valid, a drop-pick zone is created, saved to the database.
The warehouses queryset is also passed to the template to display available warehouses for selection in the form.
Since a drop-pick zone must belong to a warehouse. If the request method is not POST or the form is not valid, 
the form is displayed to the user for input.
"""
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

"""
A function to retrieve drop-pick zones from the database by querying the db by the User model
for users with the 'drop-pick' role and passing them to the 'admin/drop_pick_zones.html' template.
"""
def drop_pick_zones(request):
    drop_pick_zones = User.objects.filter(role='drop_pick_zone')
    context = {
        'drop_pick_zones': drop_pick_zones
    }
    return render(request, 'admin/drop_pick_zones.html', context)

"""
A function to handle the creation of a courier user through a form 'CourierForm'. 
The form data is validated, and if valid, a courier user is created, saved to the database
and the user is redirected to the 'admin/riders.html' page. If the request method is not POST 
or the form is not valid, the form is displayed to the user for input.
"""
def create_courier(request):
    if request.method == 'POST':
        form = CourierForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'courier'
            # Set default password for the warehouse user
            user.set_password('courier@courier')
            form.save()

            return redirect('riders')
    else:
        form = CourierForm()
    return render(request, 'admin/create_courier.html', {'form': form})
