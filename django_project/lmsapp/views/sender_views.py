from django.shortcuts import render, redirect, redirect
from django.db.models import Q, Case, When, IntegerField
from django.contrib.auth.decorators import login_required
from lmsapp.forms import PackageForm
from lmsapp.models import Package, User,Warehouse,DropPickZone
import random
import string
from lmsapp.utils import get_time_of_day
from django.shortcuts import redirect
from django.contrib import messages
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import math
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse

"""
Renders out a sender dashboard template and shows packages with the statuses 
'ongoing' & 'upcoming' that are for a specific sender.
"""
@login_required
def sender_dashboard(request):
    packages = Package.objects.filter(
        user=request.user
    ).order_by(
        # Your existing order_by logic here
    )

    greeting_message = get_time_of_day()

    # Count the number of registered packages for the logged-in user
    num_registered_packages = Package.objects.filter(user=request.user).count()

    # Retrieve the upcoming packages for the logged-in user
    upcoming_packages = Package.objects.filter(user=request.user, status='upcoming')

    context = {
        'greeting_message': greeting_message,
        'packages': packages,
        'num_registered_packages': num_registered_packages,
        'upcoming_packages': upcoming_packages,
    }

    return render(request, 'sender/sender_dashboard.html', context)

def generate_package_number():
    prefix = 'pn'
    digits = ''.join(random.choices(string.digits, k=5))
    return f'{prefix}{digits}'

# def sender_history(request):
#     return render(request, 'sender/sender_history.html', {})

def sender_history(request):
    # Retrieve the completed packages from the database
    completed_packages = Package.objects.filter(status='completed')

    return render(request, 'sender/sender_history.html', {'packages': completed_packages})
    
"""  
Handles the registration of new packages by senders, ensuring the form data is valid 
and saving the package to the database with the appropriate details.
""" 
#allow loading resources from other locations
@login_required
@xframe_options_exempt
def register_package(request):
    # import json
    from django.core.serializers.json import DjangoJSONEncoder
    api_key = settings.API_KEY
    drop_pick_zones = DropPickZone.objects.all().values()  # Retrieve users with the role of 'drop_pick_zone'

    if request.method == 'POST':
        form = PackageForm(request.POST)
        if form.is_valid():
            package = form.save(commit=False)
            package.user = request.user
            package.package_number = generate_package_number()
            
            sender_longitude = request.POST.get('sender_longitude') 
            sender_latitude = request.POST.get('sender_latitude')

            recipient_longitude = request.POST.get('recipient_longitude') 
            recipient_latitude = request.POST.get('recipient_latitude')

            package.recipient_latitude = recipient_latitude
            package.recipient_longitude = recipient_longitude
            package.sender_latitude = sender_latitude
            package.sender_longitude = sender_longitude
            
            # Check if the selected courier is already assigned to a package
            courier = package.courier
            if courier and courier.assigned_packages.exists():
                messages.error(request, 'Selected courier is already assigned to a package.')
                return redirect('register_package')
            
            package.status = 'upcoming'
            # Save the additional fields to the package object
            package.recipientIdentification = form.cleaned_data['recipientIdentification']
            package.genderType = form.cleaned_data['genderType']
            package.created_by = request.user
            package.save()

            return redirect('sender_dashboard')
        else:
            error_message = 'Error processing your request'
    else:
        form = PackageForm()
        error_message = None
    
    context = {
        'form': form, 
        'error_message': error_message, 
        'drop_pick_zones': drop_pick_zones, 
        'api_key': api_key
    }

    return render(request, 'sender/register_package.html', context)


@xframe_options_exempt
@csrf_exempt
def api(request):
    import json
    from django.http import JsonResponse
    # check wat action I am doing now
    params = {}
    #determine what type of call
    if request.method == "POST":
        params = dict(request.POST.items())
    elif request.method == "GET":
        params = dict(request.GET.items())

    # decalre reponse
    
    response = {"error":True, "error_msg":"API error occured"}
    if params.get("action","") == "":
        response["error"] = True
        response["error_msg"] = "No action specified"
    elif params.get("action","") == "get_closest_drop_pick_locations":
        # do your stuff
        if params.get("lat","") == "" or params.get("lng","") == "":
            response["error"] = True
            response["error_msg"] = "Please provide GPS data"
        else:
            response["error"] = False
            response["error_msg"] = "completed successfully "
            response["data"] = get_closest_drop_off(params.get("lat"), params.get("lng"))
    
    elif params.get("action","") == "print home":
        response["error"] = False
        response["error_msg"] = "completed successfully "
        response["data"] = "my_data"
    
    return JsonResponse(response, safe=False)

def get_closest_drop_off(lat, lng):
    #retruns a json llist of all locations
    #liooop through all drop picks
    # get distance in meteresd or kms for each droppick in comparison to GPS lat long passed
    # formulate a list of the drop pciks with those closest first
    # return this list
    closest_drop_pick_zones = []
    drop_pick_zones = DropPickZone.objects.all().values()
    for drop_pick_zone in drop_pick_zones:
        distance = calculate_distance(
            float(lat),
            float(lng),
            drop_pick_zone["latitude"],
            drop_pick_zone["longitude"]
        )
        drop_pick_zone["distance"] = distance
        closest_drop_pick_zones.append(drop_pick_zone)

    closest_drop_pick_zones.sort(key=lambda x: x["distance"])
    closest_drop_pick_zones = closest_drop_pick_zones[:5]
    # dormulate html string for lookups
    html = """<option value="" selected="" disabled="">-- Select Location ⬇️ --</option>"""
    for x in closest_drop_pick_zones:
        html += "<option value='" + str(x["id"]) + "'>" + str(x["name"]) + " (" + str(round(x["distance"], 1)) + " Kms)</option>  "

    # forumlate HTML string of all options
    return html


def calculate_distance(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Haversine formula
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = 6371 * c  # Radius of the Earth in kilometers

    return distance

@csrf_exempt
def calculate_delivery_fee(request):
    if request.method == 'POST':
        params = dict(request.POST.items())
        print("params")
        print(params)
        # Retrieve the coordinates from the POST data
        sender_latitude = float(params.get('sender_latitude', 0))
        sender_longitude = float(request.POST.get('sender_longitude', 0))
        recipient_latitude = float(request.POST.get('recipient_latitude', 0))
        recipient_longitude = float(request.POST.get('recipient_longitude', 0))

        print("Sender Latitude:", sender_latitude)
        print("Sender Longitude:", sender_longitude)
        print("Recipient Latitude:", recipient_latitude)
        print("Recipient Longitude:", recipient_longitude)

        # Calculate the distance between sender and recipient coordinates (you can reuse your existing calculate_distance function)
        distance_km = calculate_distance(sender_latitude, sender_longitude, recipient_latitude, recipient_longitude)

        print("Distance (km):", distance_km)

        # Calculate the delivery fee (assuming 1000 per kilometer)
        delivery_fee = distance_km * 500

        print("Delivery Fee:", delivery_fee)

        # Return the calculated delivery fee as a JSON response
        return JsonResponse({'delivery_fee': delivery_fee})

    return JsonResponse({'error': 'Invalid request method.'}, status=400)

