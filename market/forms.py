from django import forms

# Base signup form provided by django-allauth
from allauth.account.forms import SignupForm 


# Custom User model extending AbstractUser
from .models import User  


class CustomSignupForm(SignupForm):
    """
    Custom signup form extending django-allauth's SignupForm.
    Adds a 'nickname' and 'address' field and stores it on the custom User model.
    """

    # Extra optional nickname displayed on the signup page
    nickname = forms.CharField(max_length=15, required=True, label="Nickname")

    # Required address field displayed on the signup page
    address = forms.CharField(max_length=40, required=True, label="Address")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove all help text from password fields
        if "password1" in self.fields:
            self.fields["password1"].help_text = ""
        if "password2" in self.fields:
            self.fields["password2"].help_text = ""

    def clean_nickname(self):
        """
        Validate that the nickname is unique before saving the user.
        This replicates what a ModelForm would normally do for a unique field.
        """
        # Get the nickname value that was submitted in the form
        nickname = self.cleaned_data.get("nickname")

        # Check if any existing user already has this nickname
        if User.objects.filter(nickname=nickname).exists():
            # Raise a validation error that will be shown on the form field
            raise forms.ValidationError("This nickname is already taken.")

        # Return the validated nickname value
        return nickname

    def save(self, request):
        """
        Called by django-allauth when the signup form is submitted and valid.
        Creates the user via the parent class, then attaches 'nickname' and 'address'.
        """
        # First let allauth create the user object (email, password, etc.)
        user = super().save(request)

        # Safely get the values from the cleaned form data
        nickname = self.cleaned_data.get("nickname")
        address = self.cleaned_data.get("address")

        # Attach nickname and address to the user instance
        user.nickname = nickname  # nickname may be None/empty if not provided
        user.address = address    # address is required, so this should always be set
        user.save()

        # Return the user instance to allauth's signup flow
        return user
