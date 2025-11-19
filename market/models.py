from django.db import models

# Reusable base class for a fully featured User model
from django.contrib.auth.models import AbstractUser

# Import the field-level validator from validators.py
from .validators import validate_no_special_characters

# Validator used to enforce a minimum numeric value
from django.core.validators import MinValueValidator

# Used to create safe folder names and timestamp-based subfolders for uploads
from django.utils import timezone
from django.utils.text import slugify


# Custom user model extending Django's default AbstractUser
class User(AbstractUser):
    """Custom user model with additional fields like nickname and address."""

    # Custom optional unique nickname field for each user
    nickname = models.CharField(
        max_length=15, 
        unique=True, 
        null=True,
        validators=[validate_no_special_characters]    
    )

    # Optional address field for each user
    address = models.CharField(max_length=50, null=True)

    # Optional city field for each user
    city = models.CharField(max_length=40, null=True)

    def __str__(self):
        return self.email


def item_image_upload_to(instance, filename):
    """
    Build the upload path for item images based on the post author and creation month.

    Resulting path pattern:
    media/item_pics/<nickname-or-email-local-part>/<year-month>/<filename>

    Example:
    item_pics/podo-user/202511/my_photo.jpg
    """
    author = instance.item_author

    # Priority 1: use the user's nickname if available
    if author.nickname:
        base_name = author.nickname
        
    # Priority 2: fall back to username (email), using only the part before '@'
    elif author.username:
        base_name = author.username.split("@")[0]
        
    # Fallback name if both nickname and username are unexpectedly missing
    else:
        base_name = "user"

    # Convert the base name into a filesystem- and URL-safe slug
    folder_name = slugify(base_name)

    # Use current year+month (e.g. "202511") as a subfolder for upload date
    month_folder = timezone.now().strftime("%Y%m")

    # Final upload path relative to MEDIA_ROOT
    return f"item_pics/{folder_name}/{month_folder}/{filename}"


# Post model for items listed in the market
class PostItem(models.Model):
    """Represents a single item posted for sale in the market."""

    # Short title displayed in listings and detail pages
    item_title = models.CharField(max_length=60)

    # Item price in whole currency units (must be at least 1)
    item_price = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    #  Available condition choices for the item
    CONDITION_CHOICHES = [
        ("new", "NEW"),
        ("excellent", "EXCELLENT"),
        ("good", "GOOD"),
        ("fair", "FAIR"),
        ("poor", "POOR")
    ]

    # Condition of the item, restricted to the choices above
    item_condition = models.CharField(max_length=10, choices=CONDITION_CHOICHES, default="good")

    # Optional detailed description of the item
    item_detail = models.TextField(blank=True, null=True)

    # First image is required
    item_image1 = models.ImageField(upload_to=item_image_upload_to)

    # Second and third images are optional
    item_image2 = models.ImageField(upload_to=item_image_upload_to, blank=True, null=True)
    item_image3 = models.ImageField(upload_to=item_image_upload_to, blank=True, null=True)

    # Author of the item post (the user who created the listing)
    item_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

    # Timestamps for creation and last update
    dt_created = models.DateTimeField(auto_now_add=True)
    dt_updated = models.DateTimeField(auto_now=True)

    # Use the item title as the string representation
    def __str__(self):
        return self.item_title
