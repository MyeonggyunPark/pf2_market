from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse
from django.conf import settings

class CustomAccountAdapter(DefaultAccountAdapter):
    """
    Custom account adapter for django-allauth.

    - After login and signup, decides whether to send the user
        to the profile setup page or the home page.
    - If the profile is incomplete (missing nickname, address, or city),
        redirects to 'profile-set'.
    - Otherwise, redirects to 'home'.
    """
    def _get_profile_or_home(self, request):
        """
        Helper method that chooses between the profile setup page and home.

        - If the user is not authenticated, always redirect to 'home'.
        - If the user is authenticated but profile is incomplete,
            redirect to 'profile-set'.
        - If the profile is complete, redirect to 'home'.
        """

        user = request.user

        # Anonymous users (should rarely happen here, but safe fallback)
        if not user.is_authenticated:
            return reverse("home")

        # Profile considered incomplete if any of these fields are missing
        if not user.nickname or not user.address or not user.city:
            return reverse("profile-set")

        # Profile is complete → go to home page
        return reverse("home")

    def get_login_redirect_url(self, request):
        """
        Determine redirect URL after a successful login.

        - Uses the same logic as signup: profile first if incomplete,
            otherwise home.
        """
        return self._get_profile_or_home(request)

    def get_signup_redirect_url(self, request):
        """
        Determine redirect URL after a successful email/password signup.

        - Uses the same profile-or-home logic so that brand new users
            are guided to complete their profile first.
        """
        return self._get_profile_or_home(request)

    def send_mail(self, template_prefix, email, context):
        """
        Extend the default allauth send_mail behavior.

        - Injects EMAIL_LOGO_URL from settings into the template context so
            that HTML email templates can render a static logo via {{ email_logo_url }}.
        """

        # Provide the absolute logo URL to every email template that uses this adapter.
        context["email_logo_url"] = settings.EMAIL_LOGO_URL

        # Delegate the actual email rendering and sending to the parent implementation.
        return super().send_mail(template_prefix, email, context)
