# views.py
`from django.shortcuts import render, redirect`    
`from openpyxl import load_workbook`     
`from .models import Package`     
`from django.utils import timezone`    

```
def upload_excel(request):
    if request.method == "POST":
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = form.cleaned_data['excel_file']
            wb = load_workbook(excel_file)
            sheet = wb.active

            for row in sheet.iter_rows(min_row=2, values_only=True):
                order_id, order_date, recipient_name, delivery_address, city, phone, item, qty = row

                # Create a new Package instance
                package = Package(
                    packageName=item,
                    deliveryType='standard',  # You can set this based on your requirement
                    recipientName=recipient_name,
                    recipientEmail='',  # You can set this based on your requirement
                    recipientTelephone=phone,
                    recipientAddress=delivery_address + ', ' + city,
                    packageDescription='',
                    sendersName='',  # You can set this based on your requirement
                    sendersEmail='',  # You can set this based on your requirement
                    sendersAddress='',  # You can set this based on your requirement
                    sendersContact='',  # You can set this based on your requirement
                    created_by=request.user,
                    modified_by=request.user,
                    assigned_at=timezone.now(),
                    status='upcoming',  # You can set this based on your requirement
                )
                package.save()

            return redirect("upload_success")
    else:
        form = ExcelUploadForm()

    return render(request, "upload_form.html", {"form": form})
```
