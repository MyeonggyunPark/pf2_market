from django import forms

# Base signup form provided by django-allauth
from allauth.account.forms import SignupForm 

# Custom User model extending AbstractUser
from .models import User, PostItem  


class CustomSignupForm(SignupForm):
    """
    Custom signup form extending django-allauth's SignupForm.
    Adds a 'nickname' and 'address' field and stores it on the custom User model.
    """

    # Extra optional nickname displayed on the signup page
    nickname = forms.CharField(max_length=15, required=True, label="Nickname")

    # Required address field displayed on the signup page
    address = forms.CharField(max_length=40, required=True, label="Address")

    # Required city field displayed on the signup page
    city = forms.CharField(max_length=40, required=True, label="City")

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
        Creates the user via the parent class, then attaches 'nickname' and 'address' and 'city'.
        """
        # First let allauth create the user object (email, password, etc.)
        user = super().save(request)

        # Safely get the values from the cleaned form data
        nickname = self.cleaned_data.get("nickname")
        address = self.cleaned_data.get("address")
        city = self.cleaned_data.get("city")

        # Attach nickname and address to the user instance
        user.nickname = nickname 
        user.address = address    
        user.city = city
        user.save()

        # Return the user instance to allauth's signup flow
        return user


class BasePostItemForm(forms.ModelForm):
    """
    Base ModelForm for PostItem used by both create and update forms.

    - Renders item_condition as radio buttons.
    - Hides native file inputs for item_image1/2/3 (custom UI in template).
    - Removes HTML5 'required' so that validation is handled by Django only.
    - Reuses model-level 'blank' messages as form-level 'required' messages.
    """

    class Meta:
        # Underlying model for this form
        model = PostItem
        fields = "__all__"
        # Widgets override: render condition as radios and hide native file inputs
        widgets = {
            "item_condition": forms.RadioSelect(),
            "item_image1": forms.FileInput(attrs={"class": "hidden"}),
            "item_image2": forms.FileInput(attrs={"class": "hidden"}),
            "item_image3": forms.FileInput(attrs={"class": "hidden"}),
        }

    def __init__(self, *args, **kwargs):
        """
        Customize the default form behavior after initialization.

        -   Remove HTML 'required' attributes from all fields to prevent
            browser-side validation popups and rely solely on Django's
            server-side validation.
        -   For selected fields, copy the model's 'blank' error message
            to the form field's 'required' error, so that when the form
            reports a required-field error, it uses the same text defined
            on the model.
        """
        super().__init__(*args, **kwargs)

        # Remove HTML5 required attributes from all widgets
        for _, field in self.fields.items():
            field.widget.attrs.pop("required", None)

        # For these fields, reuse the model-level "blank" error message
        # as the form-level "required" error message.
        # This avoids hard-coding the same text in both model and form.
        for name in [
            "item_title",
            "item_price",
            "item_condition",
            "item_detail",
            "item_image1",
        ]:
            # Get the corresponding model field definition
            model_field = self._meta.model._meta.get_field(name)

            # Read the 'blank' error message from the model field
            blank_msg = model_field.error_messages.get("blank")

            # If a blank message exists, apply it to the form field's 'required' error
            if blank_msg:
                self.fields[name].error_messages["required"] = blank_msg


class PostItemCreateForm(BasePostItemForm):
    """
    Form used for creating new PostItem instances.

    Does NOT expose 'is_sold' – new items are created as unsold by default.
    """

    class Meta(BasePostItemForm.Meta):
        # Fields that will be rendered and processed in the create form
        fields = [
            "item_title",
            "item_price",
            "item_condition",
            "item_image1",
            "item_image2",
            "item_image3",
            "item_detail",
        ]


class PostItemUpdateForm(BasePostItemForm):
    """
    Form used for updating existing PostItem instances.

    Same as the create form, but includes the 'is_sold' field so that
    the seller can mark the item as sold.
    """

    class Meta(BasePostItemForm.Meta):
        # Same fields as create form + is_sold
        fields = [
            "item_title",
            "item_price",
            "item_condition",
            "item_image1",
            "item_image2",
            "item_image3",
            "item_detail",
            "is_sold",
        ]
