from django.contrib import admin

# Preconfigured admin class for user management (base class for User-like models)
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Import the custom User and PostItem models from the current app
from .models import User, PostItem


# Register the custom User model in the admin site
# and use a custom admin class that extends Django's built-in UserAdmin
@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    """
    Admin configuration for the custom User model.

    - Inherits all default user management features from Django's built-in UserAdmin.
    - Adds support for custom profile fields (nickname, address, city, profile_pic, intro).
    """

    # Extend the default fieldsets to show custom fields
    # in the change form (edit existing user in the admin)
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Custom Fields", {"fields": ("nickname", "address", "city", "profile_pic", "intro", "seller_rating")}),
    )

    # Extend the add_fieldsets to include custom fields
    # in the add form (create a new user in the admin)
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (
            "Custom Fields",
            {
                "classes": ("wide",),
                "fields": (
                    "nickname",
                    "address",
                    "city",
                    "profile_pic",
                    "intro",
                    "seller_rating",
                ),
            },
        ),
    )

    # Columns shown in the user list view in the admin.
    list_display = (
        "nickname",
        "username",
        "email",
        "seller_rating",
        "profile_pic",
        "address",
        "city",
        "is_staff",
    )


# Register the PostItem model with a basic ModelAdmin configuration
@admin.register(PostItem)
class PostItemAdmin(admin.ModelAdmin):
    """
    Admin configuration for the PostItem model.
    Provides a convenient list view and basic filters/search in the admin UI.
    """

    # Columns shown in the list view
    list_display = (
        "item_title",
        "is_sold",
        "item_price",
        "item_condition",
        "item_author",
        "dt_created",
        "dt_updated"
    )

    # Filters in the right sidebar
    list_filter = ("is_sold", "item_price","item_condition", "dt_created", "dt_updated")

    # Fields that can be searched via the search box
    search_fields = (
        "item_title",
        "item_price",
        "item_condition",
        "item_author__nickname",
        "item_author__username"
    )

    # Default ordering in the list view (newest first)
    ordering = ("-dt_created",)
