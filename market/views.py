from django.shortcuts import render
from django.urls import reverse
from allauth.account.views import PasswordChangeView


def index(request):
    """
    Simple view that renders the main index page of the 'market' app.
    """
    return render(request, "market/index.html")

class CustomPasswordChangeView(PasswordChangeView):
    """
    Custom password change view that extends django-allauth's PasswordChangeView.
    Overrides the success URL to redirect to the 'home' page after the password is changed.
    """

    def get_success_url(self):
        """
        Return the URL to redirect to after a successful password change.
        Uses reverse_lazy so the URL is resolved only when needed.
        """
        return reverse("home")
