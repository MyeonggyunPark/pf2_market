import string
from django.core.exceptions import ValidationError


def contains_special_character(value):
    """
    Check if the given value contains at least one special (punctuation) character.
    Returns True if a special character is found, otherwise False.
    """
    for char in value:
        if char in string.punctuation:
            return True
    return False


def contains_uppercase_letter(value):
    """
    Check if the given value contains at least one uppercase letter (A–Z).
    Returns True if an uppercase letter is found, otherwise False.
    """
    for char in value:
        if char.isupper():
            return True
    return False


def contains_lowercase_letter(value):
    """
    Check if the given value contains at least one lowercase letter (a–z).
    Returns True if a lowercase letter is found, otherwise False.
    """
    for char in value:
        if char.islower():
            return True
    return False


def contains_number(value):
    """
    Check if the given value contains at least one numeric digit (0–9).
    Returns True if a digit is found, otherwise False.
    """
    for char in value:
        if char.isdigit():
            return True
    return False


class CustomPasswordValidator:
    """
    Custom password validator to enforce strong password rules:
    - At least 8 characters long
    - Contains at least one uppercase letter
    - Contains at least one lowercase letter
    - Contains at least one digit
    - Contains at least one special character
    """

    def validate(self, password, user=None):
        """
        Called by Django when validating a password.
        Raises ValidationError if the password does not meet the requirements.
        """
        if (
            len(password) < 8
            or not contains_uppercase_letter(password)
            or not contains_lowercase_letter(password)
            or not contains_number(password)
            or not contains_special_character(password)
        ):
            # Raise an error if the password does not meet the required complexity
            raise ValidationError(
                "Password must be at least 8 characters long and include uppercase letters, "
                "lowercase letters, numbers, and special characters."
            )

    def get_help_text(self):
        """
        Returns a human-readable description of the password rules.
        This text is displayed in password forms (e.g., admin, registration).
        """
        return (
            "Your password must be at least 8 characters long and include uppercase letters, "
            "lowercase letters, numbers, and special characters."
        )


def validate_no_special_characters(value):
    """
    Field validator that disallows any special characters in the given value.
    Useful for fields that should only contain letters and/or numbers.
    """
    # If the value contains any special character, reject it
    if contains_special_character(value):
        raise ValidationError("Special characters are not allowed.")


def validate_image_mime_type(value):
    """
    Custom validator to ensure the uploaded file has a valid image MIME type.

    This adds an extra validation layer on top of the file extension check,
    so that files renamed to end with .jpg/.png but not actually images are rejected.
    """
    # List of allowed MIME types for uploaded image files
    valid_mime_types = ["image/jpeg", "image/png"]

    # Get the MIME type from the uploaded file object (may be None in some edge cases)
    file_mime_type = getattr(value, "content_type", None)

    # Reject the file if its MIME type is not one of the allowed image types
    if file_mime_type not in valid_mime_types:
        raise ValidationError("Only JPEG and PNG images are allowed.")
