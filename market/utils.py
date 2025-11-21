from django.utils import timezone
from django.utils.text import slugify

from django.shortcuts import redirect
from allauth.account.models import EmailAddress


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

    # Priority 2: fall back to username
    elif author.username:
        base_name = author.username

    # Fallback name if both nickname and username are unexpectedly missing
    else:
        base_name = "user"

    # Convert the base name into a filesystem- and URL-safe slug
    folder_name = slugify(base_name)

    # Use current year+month (e.g. "202511") as a subfolder for upload date
    month_folder = timezone.now().strftime("%Y%m")

    # Final upload path relative to MEDIA_ROOT
    return f"item_pics/{folder_name}/{month_folder}/{filename}"


def profile_image_upload_to(instance, filename):
    """
    Build the upload path for profile images based on the market user and creation month.

    Resulting path pattern:
    media/profile_pics/<nickname-or-email-local-part>/<year-month>/<filename>

    Example:
    profile_pics/podo-user/202511/my_profile_photo.jpg
    """

    # Priority 1: use the user's nickname if available
    if instance.nickname:
        base_name = instance.nickname

    # Priority 2: fall back to username
    elif instance.username:
        base_name = instance.username

    # Fallback name if both nickname and username are unexpectedly missing
    else:
        base_name = "user"

    # Convert the base name into a filesystem- and URL-safe slug
    folder_name = slugify(base_name)

    # Use current year+month (e.g. "202511") as a subfolder for upload date
    month_folder = timezone.now().strftime("%Y%m")

    # Final upload path relative to MEDIA_ROOT
    return f"profile_pics/{folder_name}/{month_folder}/{filename}"


def confirmation_required_redirect(self, request):
    """
    Custom redirect callback used with UserPassesTestMixin.raise_exception.

    - Ensures the logged-in user has a primary EmailAddress object.
    - If the email is not verified yet, sends a confirmation email.
    - Finally redirects to the 'email confirmation required' page.
    """
    user = request.user

    # Safely get or create the user's primary EmailAddress
    email_address, _ = EmailAddress.objects.get_or_create(
        user=user,
        email=user.email,
        defaults={"primary": True},
    )

    # If the email is not verified yet, send a confirmation email
    if not email_address.verified:
        email_address.send_confirmation(request)

    # Redirect the user to the information page
    return redirect("account_email_confirmation_required")
