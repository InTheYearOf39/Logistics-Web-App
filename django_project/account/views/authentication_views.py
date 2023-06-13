from django.shortcuts import render, redirect, redirect
from django.contrib.auth import authenticate, login, logout
from account.forms import SignUpForm, LoginForm
from django.shortcuts import redirect



def register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            msg = 'user created'

            dashboard_mapping = {
                'admin': 'admin_dashboard',
                'courier': 'courier_dashboard',
                'sender': 'sender_dashboard',
                'recipient': 'recipient_dashboard',
                'drop_pick_zone': 'drop_pick_zone_dashboard',
            }
            dashboard_url = dashboard_mapping.get(user.role)
            login(request, user)
            
            return redirect(dashboard_url)

        else:
            msg = 'form is not valid'
    else:
        form = SignUpForm()
    return render(request,'auth/register.html', {'form': form, 'msg': msg})


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                dashboard_mapping = {
                        'admin': 'admin_dashboard',
                        'courier': 'courier_dashboard',
                        'sender': 'sender_dashboard',
                        'recipient': 'recipient_dashboard',
                        'drop_pick_zone': 'drop_pick_zone_dashboard',
                    }
                dashboard_url = dashboard_mapping.get(user.role)
                if dashboard_url:
                    return redirect(dashboard_url)
            else:
                msg= 'invalid credentials'
        else:
            msg = 'error validating form'
    return render(request, 'auth/login.html', {'form': form, 'msg': msg})

def logout_user(request):
    logout(request)
    return redirect('index.html/')
