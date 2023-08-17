"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls import handler404, handler500, handler400, handler403

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('lmsapp.urls')),
    path("accounts/", include("allauth.urls")),
]

# Custom URL patterns for handling 404 and 500 errors
handler404 = 'lmsapp.views.site_views.handle_404'  #page_not_found
handler500 = 'lmsapp.views.site_views.handle_500'   #server_error
handler400 = 'lmsapp.views.site_views.handle_400'   #bad_request
handler403 = 'lmsapp.views.site_views.handle_403'   #permission_denied
