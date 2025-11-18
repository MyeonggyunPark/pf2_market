from django.contrib import admin

# Preconfigured admin class for user management (base class for User-like models)
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Import the custom User model from the current app
from .models import User


# Register the custom User model in the admin site
# and use a custom admin class that extends Django's built-in UserAdmin
@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    """
    Admin configuration for the custom User model.
    Inherits all default user management features from Django's built-in UserAdmin.
    """

    # Extend the default fieldsets to show the custom "nickname" and "address" field
    # in the change form (edit existing user in the admin)
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Custom Fields", {"fields": ("nickname", "address")}),
    )

    # Extend the add_fieldsets to include the custom "nickname" and "address" field
    # in the add form (create a new user in the admin)
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (
            "Custom Fields",
            {
                "classes": ("wide",),
                "fields": ("nickname", "address"),
            },
        ),
    )
