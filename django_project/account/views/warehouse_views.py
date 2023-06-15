from django.shortcuts import render, redirect, redirect, get_object_or_404
from account.models import Package, User
from django.shortcuts import redirect, get_object_or_404
from account.forms import WarehouseForm, DropPickForm
from django.contrib.auth.decorators import user_passes_test





@user_passes_test(lambda u: u.is_authenticated and u.role == 'warehouse')
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

        return redirect('warehouse_dashboard')

    couriers = User.objects.filter(role='courier', status='available')  # Filter couriers by status='available'

    return render(request, 'warehouse/assign_courier.html', {'package_id': package_id, 'couriers': couriers})
