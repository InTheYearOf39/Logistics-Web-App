from django.shortcuts import render, redirect
from account.utils import get_time_of_day
from django.contrib.auth.decorators import login_required


@login_required
def warehouse_dashboard(request):
    greeting_message = get_time_of_day()
    context = {
        'greeting_message': greeting_message,
    }
    return render(request, 'warehouse/warehouse_dashboard.html', context)