from django.contrib import admin

# Preconfigured admin class for user management
from django.contrib.auth.admin import UserAdmin


# Import the custom User model from the current app
from .models import User


# Register the custom User model in the admin site
# and use Django's built-in UserAdmin to get full user management features
admin.site.register(User, UserAdmin)
