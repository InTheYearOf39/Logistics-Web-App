from django.shortcuts import render, redirect, redirect
from django.db.models import Q, Case, When, IntegerField
from django.contrib.auth.decorators import login_required, user_passes_test 
from lmsapp.forms import PackageForm
from lmsapp.models import Package, User,Warehouse,DropPickZone,APIKey
import random
import string
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import math
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db import IntegrityError
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from geopy.distance import geodesic
from typing import Union


def is_sender_user(user):
    return user.role == 'sender'

"""
Renders out a sender dashboard template and shows packages with the diferent stages 
they've reached in the ecos-system by click of a button using a modal timeline.
"""
@login_required
@user_passes_test(is_sender_user)
def sender_dashboard(request):
    packages = Package.objects.filter(user=request.user).exclude(status='completed').order_by('-created_on').values()

    # loop through all rows and add a ccustom status vlauetatus_htmls for each
    for ind in range(0,len(packages)):
        status_html = """
        <div class="modal fade" id='staticBackdrop""" + str(packages[ind]["id"]) + """' data-coreui-backdrop="static" data-coreui-keyboard="false" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
                        <div class="modal-dialog modal-xl">
                          <div class="modal-content">
                            <div class="modal-header">
                              <h5 class="modal-title" id="staticBackdropLabel">Package Status</h5> 
                              <button type="button" class="btn-close" data-coreui-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body">

                                    <div class="container">
                                      <div class="row">
                                          <div class="col-md-12">
                                              <div class="card">
                                                  <div class="card-body">
                                                      <h6 class="card-title">Timeline</h6>
                                                      <div id="content">
                                                          <ul class="timeline" >
                                                              <li class='event  """ + ("active" if packages[ind]["status"] == "upcoming" else "" ) + """'  step="One" data-status="upcoming">
                                                                  <h3>Registration</h3>
                                                                  <p>Your package has been registered successfully. Awaiting to be dropped off at drop-off location.</p>
                                                              </li>
                                                              <li class='event  """ + ("active" if packages[ind]["status"] in ["dropped_off","dispatched", "en_route", "warehouse_arrival"] else "" ) + """' step="Two" data-status="dropped_off">
                                                                  <h3>Package Dropped-Off</h3>
                                                                  <p>Your package has been dropped off at the DropOff Location.</p>
                                                              </li>
                                                              <li class='event  """ + ("active" if packages[ind]["status"] in ["in_house", "in_transit", "at_pickup"] else "" ) + """' step="Three" data-status="in_house">
                                                                  <h3>At Warehouse</h3>
                                                                  <p>Your package has been dropped off at the Warehouse.</p>
                                                              </li>
                                                              <li class='event  """ + ("active" if packages[ind]["status"] in ["ready_for_pickup", "pending_delivery", "out_for_delivery", "arrived"] else "" ) + """' step="Four" data-status="ready_for_pickup">
                                                                  <h3>Package at Pick-Up location</h3>
                                                                  <p>Your package has been dropped off at the PickUp Location. It's ready for pick up.</p>
                                                              </li>
                                                              <li class='event  """ + ("active" if packages[ind]["status"] == "completed" else "" ) + """' step="Five" data-status="completed">
                                                                  <h3>Picked Up !</h3>
                                                                  <p>Thank you for choosing our services. We hope to see you soon!</p>
                                                              </li>
                                                          </ul>
                                    
                                                      </div>
                                                  </div>
                                              </div>
                                          </div>
                                      </div>
                                    </div>


                            </div>
                          </div>
                        </div>
                      </div>
        """
        # add this value to the list
        packages[ind]["status_html"] = status_html

    # Count the number of registered packages for the logged-in user
    num_registered_packages = Package.objects.filter(user=request.user).count()


    context = {
        'packages': packages,
        'num_registered_packages': num_registered_packages,
    }

    return render(request, 'sender/sender_dashboard.html', context)

def generate_package_number():
    prefix = 'PN'
    digits = ''.join(random.choices(string.digits, k=5))
    return f'{prefix}{digits}'


# @login_required
# @user_passes_test(is_sender_user)
# def sender_history(request):
#     # Retrieve the completed packages from the database
#     completed_packages = Package.objects.filter(status='completed')

#     return render(request, 'sender/sender_history.html', {'packages': completed_packages})


@login_required
@user_passes_test(is_sender_user)
def sender_history(request):
    # Retrieve the completed packages from the database

    packages = Package.objects.filter(user=request.user, status='completed').order_by('created_on').values()

    # loop through all rows and add a ccustom status vlauetatus_htmls for each
    for ind in range(0,len(packages)):
        status_html = """
        <div class="modal fade" id='staticBackdrop""" + str(packages[ind]["id"]) + """' data-coreui-backdrop="static" data-coreui-keyboard="false" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
                        <div class="modal-dialog modal-xl">
                          <div class="modal-content">
                            <div class="modal-header">
                              <h5 class="modal-title" id="staticBackdropLabel">Package Status</h5> 
                              <button type="button" class="btn-close" data-coreui-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body">

                                    <div class="container">
                                      <div class="row">
                                          <div class="col-md-12">
                                              <div class="card">
                                                  <div class="card-body">
                                                      <h6 class="card-title">Timeline</h6>
                                                      <div id="content">
                                                          <ul class="timeline" >
                                                              <li class='event  """ + ("active" if packages[ind]["status"] == "upcoming" else "" ) + """'  step="One" data-status="upcoming">
                                                                  <h3>Registration</h3>
                                                                  <p>Your package has been registered successfully. Awaiting to be dropped off at drop-off location.</p>
                                                              </li>
                                                              <li class='event  """ + ("active" if packages[ind]["status"] in ["dropped_off","dispatched", "en_route", "warehouse_arrival"] else "" ) + """' step="Two" data-status="dropped_off">
                                                                  <h3>Package Dropped-Off</h3>
                                                                  <p>Your package has been dropped off at the DropOff Location.</p>
                                                              </li>
                                                              <li class='event  """ + ("active" if packages[ind]["status"] in ["in_house", "in_transit", "at_pickup"] else "" ) + """' step="Three" data-status="in_house">
                                                                  <h3>At Warehouse</h3>
                                                                  <p>Your package has been dropped off at the Warehouse.</p>
                                                              </li>
                                                              <li class='event  """ + ("active" if packages[ind]["status"] in ["ready_for_pickup", "pending_delivery", "out_for_delivery", "arrived"] else "" ) + """' step="Four" data-status="ready_for_pickup">
                                                                  <h3>Package at Pick-Up location</h3>
                                                                  <p>Your package has been dropped off at the PickUp Location. It's ready for pick up.</p>
                                                              </li>
                                                              <li class='event  """ + ("active" if packages[ind]["status"] == "completed" else "" ) + """' step="Five" data-status="completed">
                                                                  <h3>Picked Up !</h3>
                                                                  <p>Thank you for choosing our services. We hope to see you soon!</p>
                                                              </li>
                                                          </ul>
                                    
                                                      </div>
                                                  </div>
                                              </div>
                                          </div>
                                      </div>
                                    </div>


                            </div>
                          </div>
                        </div>
                      </div>
        """
        # add this value to the list
        packages[ind]["status_html"] = status_html

    # Count the number of registered packages for the logged-in user
    num_registered_packages = Package.objects.filter(user=request.user).count()


    context = {
        'packages': packages,
        'num_registered_packages': num_registered_packages,
    }

    return render(request, 'sender/sender_history.html', context)
    
"""  
Handles the registration of new packages by senders, ensuring the form data is valid 
and saving the package to the database with the appropriate details.
""" 
#allow loading resources from other locations
@login_required
@user_passes_test(is_sender_user)
@xframe_options_exempt
def register_package(request):
    google_api_key = settings.API_KEY

    if request.method == 'POST':
        form = PackageForm(request.POST)
        if form.is_valid():
            package = form.save(commit=False)        

            sender_longitude = request.POST.get('sender_longitude') 
            sender_latitude = request.POST.get('sender_latitude')

            recipient_longitude = request.POST.get('recipient_longitude') 
            recipient_latitude = request.POST.get('recipient_latitude')

            delivery_type = form.cleaned_data["deliveryType"]
            drop_off_location = form.cleaned_data["dropOffLocation"]

            if delivery_type == 'standard' and not drop_off_location:
                form.add_error('dropOffLocation', "Drop off location is required for standard delivery.")
                return render(request, 'sender/register_package.html', {'form': form})

            # Determine eligible warehouse based on delivery type and user's location
            user_coordinates = (float(sender_latitude), float(sender_longitude))
            warehouses = Warehouse.objects.all()

            eligible_warehouses = []
            for warehouse in warehouses:
                warehouse_coordinates = (warehouse.latitude, warehouse.longitude)
                distance = geodesic(user_coordinates, warehouse_coordinates).kilometers
                if distance <= 10 and package.deliveryType in ['premium', 'express']:
                    eligible_warehouses.append(warehouse)

            if eligible_warehouses:
                selected_warehouse = eligible_warehouses[0]  # You can choose any logic to select a warehouse
                package.warehouse = selected_warehouse

            package.status = 'upcoming'
            # Save the additional fields to the package object

            package.sendersContact = form.cleaned_data["sendersContact"]
            package.packageName = form.cleaned_data["packageName"]
            package.packageDescription = form.cleaned_data["packageDescription"]
            package.deliveryType = delivery_type
            package.dropOffLocation = drop_off_location
            package.recipientName = form.cleaned_data["recipientName"]
            package.recipientEmail = form.cleaned_data["recipientEmail"]
            package.recipientTelephone = form.cleaned_data["recipientTelephone"]
            package.recipientAddress = form.cleaned_data["recipientAddress"]
            package.recipientIdentification = form.cleaned_data["recipientIdentification"]
            package.genderType = form.cleaned_data["genderType"]
            package.recipientPickUpLocation = form.cleaned_data["recipientPickUpLocation"]
            package.user = request.user
            package.recipient_latitude = recipient_latitude
            package.recipient_longitude = recipient_longitude
            package.sender_latitude = sender_latitude
            package.sender_longitude = sender_longitude
            package.package_number = generate_package_number()
            package.created_by = request.user
            package.save()

            messages.success(request, f'The package: {package.packageName} with package number {package.package_number} has been registered successfully')
            return redirect('sender_dashboard')
        else:
            return render(request, 'sender/register_package.html', {'form': form, 'api_key': google_api_key})
    else:
        form = PackageForm()
        return render(request, 'sender/register_package.html', {'form': form, 'api_key': google_api_key})


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
        # print("params")
        # print(params)
        # Retrieve the coordinates from the POST data
        sender_latitude = float(params.get('sender_latitude', 0))
        sender_longitude = float(request.POST.get('sender_longitude', 0))
        recipient_latitude = float(request.POST.get('recipient_latitude', 0))
        recipient_longitude = float(request.POST.get('recipient_longitude', 0))

        # print("Sender Latitude:", sender_latitude)
        # print("Sender Longitude:", sender_longitude)
        # print("Recipient Latitude:", recipient_latitude)
        # print("Recipient Longitude:", recipient_longitude)

        # Calculate the distance between sender and recipient coordinates (you can reuse your existing calculate_distance function)
        distance_km = calculate_distance(sender_latitude, sender_longitude, recipient_latitude, recipient_longitude)

        # print("Distance (km):", distance_km)

        # Calculate the delivery fee (assuming 1000 per kilometer)
        delivery_fee = distance_km * 500

        # print("Delivery Fee:", delivery_fee)

        # Return the calculated delivery fee as a JSON response
        return JsonResponse({'delivery_fee': delivery_fee})

    return JsonResponse({'error': 'Invalid request method.'}, status=400)


@csrf_exempt
def receive_data_view(request):
    
    # print(f"request: {request.headers}")
    api_req = request.headers.get('X-Api-Key', "")
    # print(api_req)
    content_type = request.META.get('CONTENT_TYPE')

    if api_req == "":
        return JsonResponse({'error': 'Provide API key'}, status=401)
    
    api_obj =  APIKey.objects.filter(api_key=api_req)
    api_key = None
    # print(f"fetched key is: {api_obj}")
    
        
    if api_obj.__len__() == 0:
        return JsonResponse({'error': 'Invalid API key'}, status=401)
    else:
        api_key = api_obj[0]

    # print(f"fetched key is: {api_key.api_key}")

           
    if content_type != 'application/json':
        return JsonResponse({'error': 'Invalid content type'}, status=400)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            for field in data:
                if isinstance(data[field], str):
                    data[field] = data[field].strip()

            expected_data_types = {
                "recipientName": str,
                "recipientEmail": str,
                "recipientAddress": str,
                "recipientContact": str,
                # "recipientIdentification": str, 
                # #this is the required field and we shall have to revert to it,
                # have used the one below just to allow mordern coast system to test since they dont capture ids at the moment

                "recipientIdentification": Union[str, None],
                "packageName": str,
                "packageDescription": str,
                "packageNumber": str,
                "sendersName": str,
                "sendersEmail": str,
                "sendersAddress": str,
                "sendersContact": str,
            }

            for field, expected_type in expected_data_types.items():
                value = data.get(field)
                if not isinstance(value, expected_type):
                    return JsonResponse({'error': f'{field} must be a {expected_type.__name__}'}, status=400)
                
            for x in [
                "recipientName", "recipientAddress", "recipientContact","packageName","sendersContact",
                "packageDescription", "packageNumber", "sendersName","sendersAddress" 
            ]:
                if data.get(x, "") == "":
                    return JsonResponse({'error': f'{x} is required'}, status=400)
                                  
            recipient_name = data.get('recipientName')
            recipient_email = data.get('recipientEmail')
            recipient_address = data.get('recipientAddress')
            recipient_contact = data.get('recipientContact')
            recipient_ID = data.get('recipientIdentification', None)
            package_name = data.get('packageName')
            package_description = data.get('packageDescription')
            package_number = data.get('packageNumber')

            sender_name = data.get('sendersName')
            sender_email = data.get('sendersEmail')
            sender_address = data.get('sendersAddress')
            sender_contact = data.get('sendersContact')
               
            try:
                validate_email(recipient_email)
                validate_email(sender_email)
            except ValidationError:
                return JsonResponse({'error': 'Invalid email format'}, status=400)
                     
             
            package = Package(
                user=api_key.user,
                packageName=package_name,
                deliveryType='premium', 
                packageDescription=package_description,
                recipientName=recipient_name,
                recipientEmail=recipient_email,
                recipientTelephone=recipient_contact,
                recipientAddress=recipient_address,
                recipientIdentification=recipient_ID,
                sendersName=sender_name,
                sendersEmail=sender_email,
                sendersAddress=sender_address,
                sendersContact=sender_contact,
                package_number=package_number,
                status='warehouse_arrival'
            )

            package.save()
            response_data = {
                'response': {
                    'success': True,
                    'data': {
                    "recipientName" : recipient_name,
                    "recipientEmail" :recipient_email,
                    "recipientAddress" : recipient_address, 
                    "recipientContact" : recipient_contact,
                    "recipientIdentification" : recipient_ID,
                    "packageName" : package_name,
                    "packageDescription" : package_description,
                    "packageNumber" : package_number,
                    "sendersName" : sender_name,
                    "sendersEmail" : sender_email,
                    "sendersAddress" : sender_address,
                    "sendersContact" : sender_contact
                    }
                }
            }

            return JsonResponse(response_data, status=200)
        
        except ValueError as ve:
            return JsonResponse({'error': str(ve)}, status=400)
        except IntegrityError as ie:
                if 'UNIQUE constraint failed: lmsapp_package.package_number' in str(ie):
                    return JsonResponse({'error': 'Package number already exists'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)
