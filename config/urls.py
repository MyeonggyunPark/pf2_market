"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from django.views.generic import TemplateView

from market.views import CustomPasswordChangeView


urlpatterns = [
    # Route for the Django admin interface
    path("admin/", admin.site.urls),

    # Include URLs for the local "market" app at the root path
    path("", include("market.urls")),
        
    # Route shown after a successful email confirmation
    path(
        "email-confirmation-done/",
        TemplateView.as_view(template_name="account/email_confirmation_done.html"),
        name="account_email_confirmation_done",
    ),
    
    # Route for changing the user's password using the custom password change view
    path(
        "password/change/",
        CustomPasswordChangeView.as_view(),
        name="account_password_change",
    ),
    
    # Include all django-allauth authentication URLs
    path("", include("allauth.urls")),
]
