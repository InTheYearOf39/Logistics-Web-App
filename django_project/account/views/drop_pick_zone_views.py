from django.shortcuts import render, redirect
from account.models import Package, User
from account.utils import get_time_of_day
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404

@login_required
@login_required
def drop_pick_zone_dashboard(request):
    drop_pick_zone = request.user
    packages = Package.objects.filter(dropOffLocation=drop_pick_zone)
    greeting_message = get_time_of_day()
    context = {
        'greeting_message': greeting_message,
        'packages': packages,
    }
    return render(request, 'drop_pick_zone/drop_pick_zone.html', context)


