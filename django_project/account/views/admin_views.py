from django.shortcuts import render, redirect, redirect, get_object_or_404
from django.db.models import Q, Case, When, IntegerField
from account.utils import get_time_of_day
from account.models import Package, User
from account.utils import get_time_of_day
from django.shortcuts import redirect, get_object_or_404



def admin(request):
    packages = Package.objects.filter(
        Q(status='ongoing') | Q(status='dropped_off') | Q(status='upcoming') 
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
        elif delivery_type == 'premium':
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
        if package.deliveryType == 'standard' and package.status == 'dropped_off':
            package.status = 'ongoing'
        elif package.deliveryType == 'premium' and package.status == 'upcoming':
            package.status = 'ongoing'

        package.save()

        # Update the courier status to "on-trip" only if they were not already on-trip
        if previous_courier_status != 'on-trip':
            courier.status = 'on-trip'
            courier.save()

        return redirect('admin_dashboard')

    couriers = User.objects.filter(role='courier', status='available')  # Filter couriers by status='available'

    return render(request, 'admin/assign_courier.html', {'package_id': package_id, 'couriers': couriers})


""" def assign_courier(request, package_id):
    package = get_object_or_404(Package, id=package_id)
    
    if request.method == 'POST':
        courier_id = request.POST.get('courier')
        courier = get_object_or_404(User, id=courier_id, role='courier')
        
        previous_courier_status = courier.status  # Save the previous status
        
        package.courier = courier
        package.status = 'ongoing'
        package.save()
        
        # Update the courier status to "on-trip" only if they were not already on-trip
        if previous_courier_status != 'on-trip':
            courier.status = 'on-trip'
            courier.save()
        
        return redirect('admin_dashboard')  
    
    couriers = User.objects.filter(role='courier', status='available')  # Filter couriers by status='available'
    
    return render(request, 'admin/assign_courier.html', {'package_id': package_id, 'couriers': couriers})
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

def admin_history(request):
    packages = Package.objects.filter(
        Q(status='completed')
    )
    context = {
        'packages': packages
    }
    return render(request, 'admin/admin_history.html', context)
