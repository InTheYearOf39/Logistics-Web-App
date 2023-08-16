from lmsapp.models import Package 

def new_premium_packages_count(request):
    new_premium_packages_count = 0
    
    if request.user.is_authenticated:
        new_premium_packages_count = Package.objects.filter(
            deliveryType='premium', status='upcoming', warehouse=request.user.warehouse
        ).count()
    
    return {'new_premium_packages_count': new_premium_packages_count}

def new_express_packages_count(request):
    new_express_packages_count = 0
    
    if request.user.is_authenticated:
        new_express_packages_count = Package.objects.filter(
            deliveryType='express', status='upcoming', warehouse=request.user.warehouse
        ).count()
    
    return {'new_express_packages_count': new_express_packages_count}
