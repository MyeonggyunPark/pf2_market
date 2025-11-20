from django.shortcuts import render
from django.urls import reverse

from allauth.account.views import PasswordChangeView
from django.views.generic import ListView, DetailView, CreateView

from .models import PostItem
from .forms import PostItemForm


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


class IndexView(ListView):
    """
    Class-based list view that renders the main home page for the market.

    - Uses PostItem as the underlying model.
    - Renders the 'market/index.html' template.
    - Exposes the object list in the template as 'items'.
    - Paginates the list, showing 4 items per page.
    - Orders items by creation date in descending order (newest first).
    """

    # The model providing the queryset for this list view
    model = PostItem

    # Template used to render the list of items
    template_name = "market/index.html"

    # Context variable name used in the template to access the object list
    context_object_name = "items"

    # Number of items displayed per page
    paginate_by = 8

    # Default ordering for the queryset (most recently created items first)
    ordering = ["-dt_created"]


class ItemDetailView(DetailView):
    """
    Class-based detail view for a single PostItem.

    - Uses PostItem as the underlying model.
    - Renders the 'market/item_detail.html' template.
    - Retrieves a single item based on the 'id' parameter from the URL.
    """

    # The model that this detail view will retrieve a single instance of
    model = PostItem

    # Template used to render the detail page for a single item
    template_name = "market/item_detail.html"

    # Name of the URL keyword argument used to look up the object (e.g. path('item/<int:id>/'))
    pk_url_kwarg = "id"


class ItemCreateView(CreateView):
    """
    Class-based create view for posting a new item to the market.

    - Uses PostItem as the underlying model.
    - Uses PostItemForm to render and validate the form fields.
    - Renders the 'market/item_form.html' template.
    - Automatically sets the current logged-in user as the item_author.
    - After a successful create, redirects to the item detail page for the new item.
    """

    # The model that will be created when the form is submitted successfully
    model = PostItem

    # The ModelForm used to render and validate input for a new PostItem
    form_class = PostItemForm

    # Template used to render the "create item" form page
    template_name = "market/item_form.html"

    def form_valid(self, form):
        """
        Called when the submitted form is valid.

        - Assigns the current logged-in user as the author of the item.
        - Then delegates to the parent implementation to save the object.
        """
        # Attach the currently authenticated user as the item author
        form.instance.item_author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        """
        Return the URL to redirect to after successfully creating a new item.

        - Redirects to the item detail page using the newly created object's ID.
        """
        return reverse("item-detail", kwargs={"id": self.object.id})
