from django.shortcuts import redirect
from django.urls import reverse


class ProfileRequiredMiddleware:
    """
    Middleware that forces authenticated users to complete their profile.

    - If a logged-in user has an incomplete profile 
        (missing nickname, address, or city), 
        almost every request is redirected to 'profile-set'.
    - Static / media requests and a small set of auth-related paths are
        excluded from the redirect.
    """

    def __init__(self, get_response):
        # One-time configuration and initialization.
        # Django passes the next callable in the middleware chain.
        self.get_response = get_response

    def __call__(self, request):
        """
        Called on every request.

        - Checks the current user and path.
        - If the user is authenticated but profile is incomplete and the
            request path is not in the exempt list, redirect to 'profile-set'.
        """
        user = request.user

        if user.is_authenticated:
            # Profile is considered incomplete if any of these fields are missing
            incomplete = not user.nickname or not user.address or not user.city

            if incomplete:
                path = request.path

                # Paths that are allowed even when the profile is incomplete
                exempt_paths = {
                    reverse("profile-set"),
                    reverse("account_logout"),
                    reverse("account_login"),
                    reverse("account_signup"),
                }

                # Redirect if the current path is not exempt and is not a static/media file
                if (
                    path not in exempt_paths
                    and not path.startswith("/static/")
                    and not path.startswith("/media/")
                ):
                    return redirect("profile-set")

        # If profile is complete or user is anonymous, continue the normal flow
        return self.get_response(request)
