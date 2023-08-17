from django.shortcuts import render, redirect, redirect
from lmsapp.models import Package, User
import random
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from lmsapp.utils import send_sms



"""
A function to render the courier dashboard. It retrieves the assigned packages for the logged in courier 
and passes them to the template along with a greeting message. Relevant information is then displayed
to the courier on their dashboard.
"""
def courier_dashboard(request):
    assigned_packages = Package.objects.filter(courier=request.user, status__in=['dispatched', 'ongoing', 'arrived', 'en_route', 'warehouse_arrival', 'in_transit', 'at_pickup'])
    context = {
        'assigned_packages': assigned_packages,
    }
    return render(request, 'courier/courier_dashboard.html', context)

"""
A function to handle the notification of package arrival at the warehouse. When the view is accessed with a POST request, 
the package is retrieved by it's package id and then the package status is updated to 'warehouse_arrival', An email notification is sent to the sender and the warehouse. If the request method is not POST, it displays an error message. Finally, the user is redirected to the courier dashboard.
 """
def notify_arrival(request, package_id):
    try:
        if request.method == 'POST':
            package = get_object_or_404(Package, pk=package_id)
            package.status = 'warehouse_arrival'
            package.save()

            # Send an email notification if recipientEmail is available
            if package.recipientEmail:
                subject = 'Package Warehouse Arrival'
                message = f"Dear sender, your package has been successfully arrived at the warehouse.\n\n"\
                            f"If you have any questions, please contact our customer support team.\n"\
                            f"Package Number: {package.package_number}\n"\
                            f"Recipient: {package.recipientName}\n"\
                            f"Recipient Address: {package.recipientAddress}\n"

                if package.dropOffLocation:
                    message += f"Drop-off Location: {package.dropOffLocation.name}\n"

                message += f"Status: {package.status}"
                
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [package.recipientEmail]

                # Try sending the email
                try:
                    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                    messages.success(request, "Package arrival notified successfully.")
                except BadHeaderError as e:
                    messages.error(request, f"Error: BadHeaderError - {str(e)}")
                except Exception as e:
                    messages.error(request, f"Error: {str(e)}")
            else:
                messages.warning(request, "Recipient email not available. Notification not sent.")
        else:
            messages.error(request, "Invalid request.")

    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")

    return redirect("courier_dashboard") # Replace with the appropriate URL


"""
A function to handle the notification of package drop-off. When the view is accessed with a POST request, a package is retrieved by its id and it's status updated to 'at_pickup'. The user is then redirected to the courier dashboard.
"""
def notify_dropoff_delivery(request, package_id):
    package = get_object_or_404(Package, id=package_id)

    if request.method == 'POST':
        # Update the package status to 'at_pickup'
        package.status = 'at_pickup'
        package.save()

        # Add any additional functionality or notifications here

        messages.success(request, "Package drop-off notified successfully.")
        return redirect('courier_dashboard')



"""
A function to handle notifying the recipient of a package arrival by sending an email with the OTP. A package is retrieved by its package id, then a random integer is generated and stored in a variable 'otp'. The otp is then associated to the package and the package is saved, The email is then sent and the the package status is updated from 'ongoing' to 'arrived'. The user is then redirected to the courier dashboard.
 """
def notify_recipient(request, package_id):
    package = get_object_or_404(Package, id=package_id) 
    print(package)
    if request.method == 'POST':
        # Check if the package deliveryType is premium
        if package.deliveryType in ['premium', 'express']:
         # Update the package status to 'arrived' for 'premium' and 'express' delivery types
           package.status = 'arrived'

        # Generate OTP
        otp = random.randint(100000, 999999)

        # Save the OTP in the package
        package.otp = otp
        package.save()

        subject = 'Package Arrival'
        message = f"Dear customer, your package has arrived. Please find the One Time Password (OTP) for your package below:\n\n"\
                  f"OTP: {package.otp}\n\n"\
                  f"Package Number: {package.package_number}, Recipient: {package.recipientName}, Status: {package.status}\n"\
                  
        # if package.dropOffLocation:
        #     message += f"Drop-off Location: {package.dropOffLocation.name}\n"

        # message += f"Status: {package.status}"

        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [package.recipientEmail]


        recipient_telephone = str(package.recipientTelephone).strip()

        if len(recipient_telephone) == 10 and recipient_telephone.startswith('0'):
            recipient_telephone = '+256' + recipient_telephone[1:]

        send_sms([recipient_telephone], message, settings.AFRICASTALKING_SENDER)
        
        try:
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            messages.success(request, "Package drop-off notified successfully.")
        except BadHeaderError as e:
            # Handle the BadHeaderError
            messages.error(request, f"Error: BadHeaderError - {str(e)}")
        except Exception as e:
            # Handle other exceptions
            messages.error(request, f"Error: {str(e)}")

        # Add any additional functionality or notifications here
        return redirect('courier_dashboard')


"""
A function to handle confirming the delivery of a package by checking the entered OTP. 
If the entered OTP matches the stored OTP and the package status is 'arrived', the package status is updated to 'completed', a success message is displayed, and the associated courier's status is updated from 'on-trip' to 'available. If the entered OTP is invalid, an error message is displayed. The user is then redirected to the courier dashboard.
"""
def confirm_delivery(request, package_id):
    if request.method == 'POST':
        package = Package.objects.get(pk=package_id)
        entered_code = request.POST.get('inputField')

        if package.status == 'arrived' and package.otp == entered_code:
            package.status = 'completed'
            package.save()
            messages.success(request, "Package delivery confirmed successfully.")
        else:
            messages.error(request, "Invalid OTP. Please try again.")
            
        courier = package.courier
        if courier:
            courier.status = 'available'
            courier.save()


    return redirect('courier_dashboard')  # Replace with the appropriate URL


"""
A function to retrieve the completed packages assigned to the current courier and display them in the courier history template. i.e Packages with the status 'completed' The greeting message and the assigned packages are passed to the template through the context.
"""
def courier_history(request):
    assigned_packages = Package.objects.filter(courier=request.user, status__in=['completed'])
    context = {
        'assigned_packages': assigned_packages,
    }
    return render(request, 'courier/courier_history.html', context)