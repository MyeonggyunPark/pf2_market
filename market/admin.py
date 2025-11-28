from django.contrib import admin

# Preconfigured admin class for user management (base class for User-like models)
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.contenttypes.admin import GenericTabularInline

# Import all Models from the current app
from .models import User, PostItem, Comment, Like


class CommentInline(admin.TabularInline):
    """
    Inline admin for comments.

    - Displays comments related to the parent object.
    - Used in PostItemAdmin to show comments received on a post.
    - Used in UserAdmin to show comments written by the user (via 'author' FK).
    """
    model = Comment

    # Removes empty input rows to keep the UI clean
    extra = 0 

    # Prevent editing creation timestamps
    readonly_fields = ("dt_created",) 


class LikeUserInline(admin.TabularInline):
    """
    Inline admin for likes *given* by a user.

    - Used in UserAdmin.
    - Connects via the 'author' ForeignKey in the Like model.
    - Shows a list of items/comments the user has liked.
    """
    model = Like

    # Explicitly specifies the ForeignKey to User
    fk_name = "author"  
    extra = 0
    verbose_name = "Given Like"
    verbose_name_plural = "Given Likes"


class LikePostInline(GenericTabularInline):
    """
    Inline admin for likes *received* by an object (e.g., PostItem).

    - Used in PostItemAdmin.
    - Must use GenericTabularInline because Like is connected via GenericForeignKey
        (content_type + object_id), not a direct ForeignKey to PostItem.
    """
    model = Like
    ct_field = "content_type" 
    fk_field = "object_id"
    extra = 0
    verbose_name = "Received Like"
    verbose_name_plural = "Received Likes"


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

    # Inlines to show related data
    # CommentInline: Shows comments authored by this user (based on Comment.author)
    # LikeUserInline: Shows likes clicked by this user (based on Like.author)
    inlines = (CommentInline, LikeUserInline )


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

    # Inlines to show interaction data
    # CommentInline: Shows comments attached to this post (based on Comment.post_item)
    # LikePostInline: Shows likes received by this post (via GenericForeignKey)
    inlines = (CommentInline, LikePostInline)

# Register the Comment model to manage comments via the admin interface
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Comment model.
    Displays a custom string representation along with timestamps.
    """

    # Columns shown in the list view.
    # 'comment_info' is a custom method defined below.
    list_display = ("comment_info", "dt_created", "dt_updated")

    # Custom method to display the model's __str__ representation in the list view.
    # The 'description' argument sets the column header name in the admin UI.
    @admin.display(description="Comment Info")
    def comment_info(self, obj):
        return str(obj)


# Register the Like model to view who liked what
@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Like model.
    Shows the user and the string representation of the liked object.
    """

    # Columns shown in the list view
    list_display = ("like_info", "dt_created")

    # Custom method to display a summary of the like instance
    @admin.display(description="Like Info")
    def like_info(self, obj):
        return str(obj)
