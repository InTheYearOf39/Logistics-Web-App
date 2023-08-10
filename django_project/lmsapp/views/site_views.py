import calendar
from django.db.models import Count
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render
from lmsapp.models import Package, User
from django.db.models.functions import ExtractDay



def index(request):
    return render(request, 'index.html', {})

def about(request):
    return render(request, 'about.html', {})

def services(request):
    return render(request, 'services.html', {})

def contact(request):
    return render(request, 'contact.html', {})

def home(request):
    return render(request, 'home.html', {})

def handle_404(request, exception):
    return render(request, '404.html', status=404)

def handle_500(request):
    return render(request, '500.html', status=500)

def handle_403(request, exception):
    return render(request, '403.html', status=403)

def handle_400(request, exception):
    return render(request, '400.html', status=400)

def home_register(request):
    return render(request, 'home_register.html', {})

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

    # percentage_delivered_day = (total_delivered_packages_day / total_packages_day) * 100
    if total_packages_day != 0:
        percentage_delivered_day = (total_delivered_packages_day / total_packages_day) * 100
        percentage_delayed_day = (total_delayed_packages_day / total_packages_day) * 100
    else:
        percentage_delivered_day = 0  # or any other appropriate value
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
    return render(request, 'admin/master_dashboard.html', context)