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
