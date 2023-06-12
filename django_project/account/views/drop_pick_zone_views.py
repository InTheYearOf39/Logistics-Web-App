from django.shortcuts import render, redirect
from account.models import Package, User
from django.contrib.auth.decorators import login_required

@login_required
def drop_pick_zone_dashboard(request):
    return render(request, 'drop_pick_zone/drop_pick_zone.html')