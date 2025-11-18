from django import forms

# Base signup form provided by django-allauth
from allauth.account.forms import SignupForm 


# Custom User model extending AbstractUser
from .models import User  


class CustomSignupForm(SignupForm):
    """
    Custom signup form extending django-allauth's SignupForm.
    Adds a 'nickname' field and stores it on the custom User model.
    """

    # Extra field displayed on the signup page (optional nickname for each user)
    nickname = forms.CharField(
        max_length=15,
        required=False,
        label="Nickname",
    )

    def save(self, request):
        """
        Called by django-allauth when the signup form is submitted and valid.
        Creates the user via the parent class, then attaches 'nickname'.
        """
        # First let allauth create the user object (email, password, etc.)
        user = super().save(request)

        # Safely get the nickname value from the cleaned form data
        nickname = self.cleaned_data.get("nickname")

        # Only update and save the user if a nickname was provided
        if nickname:
            user.nickname = nickname
            user.save()

        # Return the user instance to allauth's signup flow
        return user
