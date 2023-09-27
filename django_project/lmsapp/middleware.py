from django.shortcuts import redirect
from django.urls import reverse

class PasswordChangeMiddleware:
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        # Define a list of URL patterns that are exempt from password change
        # Add URLs that don't require authentication here
        exempt_urls = [reverse('login_view'), reverse('register'), reverse('home'), reverse('services'), reverse('about'), reverse('contact'), reverse('password_change')]

        if user.is_authenticated:
            enforced_roles = ['courier', 'warehouse', 'drop_pick_zone']
            
            # Check if the user's role is in the list of enforced roles
            if user.role in enforced_roles and not user.has_set_password:
                current_path = request.path
                if current_path not in exempt_urls:
                    return redirect(reverse('password_change'))  # Redirect to password change page
            
            dashboard_mapping = {
                'sender': 'sender_dashboard',
                'admin': 'admin_dashboard',
            }
            
            dashboard_url = dashboard_mapping.get(user.role)
            
            if dashboard_url:
                return redirect(dashboard_url)

        response = self.get_response(request)
        return response
