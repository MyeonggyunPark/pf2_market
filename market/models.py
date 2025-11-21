from django.db import models

# Reusable base class for a fully featured User model
from django.contrib.auth.models import AbstractUser

# Import the field-level validator from validators.py
from market.validators import validate_no_special_characters, validate_image_mime_type

# Reusable upload path builders for user profile images and item images
from market.utils import item_image_upload_to, profile_image_upload_to

#  Core validators for numeric ranges and file extensions
from django.core.validators import MinValueValidator, FileExtensionValidator


# Custom user model extending Django's default AbstractUser
class User(AbstractUser):
    """
    Custom user model that extends Django's AbstractUser.

    Adds:
    - nickname: unique display name shown in the UI
    - address, city: basic location information
    - profile_pic: user avatar image with a sensible default
    - intro: short user bio shown on the profile page
    """

    # Optional unique nickname field for each user
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

    # Profile picture shown on the user's profile and listings
    # Uses a default image and uploads to a per-user folder via profile_image_upload_to()
    profile_pic = models.ImageField(default="default_profile_pic.jpg", upload_to=profile_image_upload_to)

    # Short self-introduction text shown on the profile page
    intro = models.CharField(max_length=60, blank=True)

    # Available 1–5 rating choices for the seller rating
    RATING_CHOICES = [
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
    ]
    # Seller rating score (1–5) used to display seller reputation (e.g. stars)
    # Defaults to 1 for newly created users
    seller_rating = models.CharField(max_length=5, choices=RATING_CHOICES, default=1)

    def __str__(self):
        return self.email


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
