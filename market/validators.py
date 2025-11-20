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
    Custom validator to ensure the uploaded file has an image MIME type.

    This validator is intended to be used together with FileExtensionValidator:
    - FileExtensionValidator checks the file extension (e.g. .jpg, .jpeg, .png).
    - This validator checks the MIME type and ensures it starts with "image/".

    If the MIME type is missing, the check is skipped and other validators
    (such as ImageField's internal validation) are expected to handle it.

    When the MIME type does not indicate an image, a ValidationError is raised
    with the code "invalid_image" so that model or form error_messages can
    provide a user-friendly message.
    """
    # Try to read the MIME type from the uploaded file (may be empty in some cases)
    raw_mime = getattr(value, "content_type", "") or ""
    
    # Normalize the MIME type: remove any parameters (e.g. "; charset=binary") and lowercase it
    mime = raw_mime.split(";")[0].lower()

    # If no MIME type is available, skip this check and let other validators handle the file
    if not mime:
        return

    # Reject the file if its MIME type does not indicate an image
    if not mime.startswith("image/"):
        raise ValidationError(code="invalid_image")
