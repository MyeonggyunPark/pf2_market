from django.shortcuts import redirect
from allauth.account.models import EmailAddress


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
