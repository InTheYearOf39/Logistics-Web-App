from django.contrib import admin
from .models import User
from .models import Package, DropPickZone, Warehouse

# Register your models here.
admin.site.register(User)
admin.site.register(Package)
admin.site.register(DropPickZone)
admin.site.register(Warehouse)