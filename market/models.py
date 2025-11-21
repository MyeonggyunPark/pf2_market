from django.db import models

# Reusable base class for a fully featured User model
from django.contrib.auth.models import AbstractUser

# Import the field-level validator from validators.py
from .validators import validate_no_special_characters, validate_image_mime_type

# Validators used to enforce minimum numeric values and restrict allowed file extensions
from django.core.validators import MinValueValidator, FileExtensionValidator

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


## Post model for items listed in the market
class PostItem(models.Model):
    """
    Represents a single item posted for sale in the market.

    Each PostItem instance corresponds to one listing created by a user and
    includes basic information such as title, price, condition, description,
    images and author, along with timestamps.
    """

    # Short title displayed in item listings and on the detail page
    item_title = models.CharField(
        max_length=60,
        error_messages={
            "blank": "Please enter a title for your item.",
            "max_length": "Title is too long.",
            "invalid": "Please enter a valid title.",
        },
    )

    # Item price in whole currency units
    item_price = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        error_messages={
            "blank": "Please enter a price for your item.",
            "invalid": "Please enter a valid number.",
            "min_value": "Price must be at least 1 €.",
        },
    )

    # Available condition choices for the item
    # These values are stored in the database and rendered as a select/radio in forms.
    CONDITION_CHOICES = [
        ("new", "NEW"),
        ("excellent", "EXCELLENT"),
        ("good", "GOOD"),
        ("fair", "FAIR"),
        ("poor", "POOR"),
    ]

    # Condition of the item, restricted to the choices above.
    item_condition = models.CharField(
        max_length=10,
        choices=CONDITION_CHOICES,
        default=None,
        error_messages={
            "blank": "Please select a condition for your item.",
            "invalid_choice": "Invalid condition selected.",
        },
    )

    # Detailed description of the item shown on the detail page.
    item_detail = models.TextField(
        error_messages={
            "blank": "Please enter a description for your item.",
            "invalid": "Please enter a valid description.",
        },
    )

    # Whether this item has been sold (used to display sold status / styling)
    is_sold = models.BooleanField(default=False)
    
    # Main image for the item (required).
    item_image1 = models.ImageField(
        upload_to=item_image_upload_to,
        
        # Validate by file extension first, then by actual MIME type for extra safety
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png"],
                message="Please upload a JPEG or PNG image.",
            ),
            validate_image_mime_type,
        ],
        
        # Custom error message when the uploaded file is not recognized as a valid image
        error_messages={
            "blank": "Please upload a main image for your item.",
            "invalid": "Please upload a valid image file.",
            "invalid_image": "Please upload a valid JPEG or PNG image.",
        },
    )

    # Second and third images are optional.
    item_image2 = models.ImageField(
        upload_to=item_image_upload_to,
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png"],
                message="Please upload a JPEG or PNG image.",
            ),
            validate_image_mime_type,
        ],
        error_messages={
            "invalid": "Please upload a valid image file.",
            "invalid_image": "Please upload a valid JPEG or PNG image.",
        },
    )

    item_image3 = models.ImageField(
        upload_to=item_image_upload_to,
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png"],
                message="Please upload a JPEG or PNG image.",
            ),
            validate_image_mime_type,
        ],
        error_messages={
            "invalid": "Please upload a valid image file.",
            "invalid_image": "Please upload a valid JPEG or PNG image.",
        },
    )

    # Author of the item post
    item_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

    # Timestamps
    dt_created = models.DateTimeField(auto_now_add=True)
    dt_updated = models.DateTimeField(auto_now=True)

    # Use the item title as the string representation in admin and shell.
    def __str__(self):
        return self.item_title
