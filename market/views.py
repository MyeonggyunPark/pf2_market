from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from allauth.account.views import PasswordChangeView
from allauth.account.models import EmailAddress
from django.views import View
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from braces.views import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import FormMixin
from django.contrib.contenttypes.models import ContentType

from market.models import PostItem, User, Comment, Like
from market.forms import PostItemCreateForm, PostItemUpdateForm , ProfileForm, CommentForm
from market.utils import confirmation_required_redirect


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    """
    Custom password change view for logged-in users.

    - Requires authentication via LoginRequiredMixin.
    - Extends django-allauth's PasswordChangeView.
    - After a successful password change, redirects to the user's profile page.
    """

    def get_success_url(self):
        """
        Return the URL to redirect to after a successful password change.

        - Redirects to the profile detail page for the current user.
        """
        return reverse("profile", kwargs=(({"id": self.request.user.id})))


class IndexView(ListView):
    """
    Class-based list view that renders the main home page for the market.

    - Uses PostItem as the underlying model.
    - Renders the 'market/index.html' template.
    - Exposes the object list in the template as 'items'.
    - Paginates the list, showing 8 items per page.
    - Shows only items that are not marked as sold (is_sold=False).
    - Ordering is handled implicitly by PostItem.Meta (newest first).
    """

    # The model providing the queryset for this list view
    model = PostItem

    # Template used to render the list of items
    template_name = "market/index.html"

    # Context variable name used in the template to access the object list
    context_object_name = "items"

    # Number of items displayed per page
    paginate_by = 8

    def get_queryset(self):
        """
        Return the queryset for the index page.

        - Filters out items that are already sold (is_sold=True).
        - Default ordering (-dt_created) is applied by the model.
        """

        return PostItem.objects.filter(is_sold=False)


class ItemDetailView(LoginRequiredMixin, FormMixin, DetailView):
    """
    Class-based detail view for a single PostItem.

    - Requires the user to be logged in (via LoginRequiredMixin).
    - Uses PostItem as the underlying model.
    - Renders the 'market/item_detail.html' template.
    - Retrieves a single item based on the 'id' parameter from the URL.

    Form Handling (Comment):
    - Integrates FormMixin to handle the comment submission form on the same page.
    - Uses CommentForm to validate and save new comments.
    - Handles POST requests to save comments and re-render the page on errors.
    """

    # The model that this detail view will retrieve a single instance of
    model = PostItem

    # Template used to render the detail page for a single item
    template_name = "market/item_detail.html"

    # Name of the URL keyword argument used to look up the object (e.g. path('item/<int:id>/'))
    pk_url_kwarg = "id"

    # The form class to use for comment submission (processed by FormMixin)
    form_class = CommentForm 

    def get_context_data(self, **kwargs):
        """
        Extend the default context with the comment form.

        - Adds 'form' to the context so it can be rendered in the template.
        - Uses self.get_form() to ensure the form is correctly instantiated
            (with data on POST, empty on GET).
        """
        context =  super().get_context_data(**kwargs)
        context["form"] = self.get_form()
        context['postitem_ctype_id'] = ContentType.objects.get(model='postitem').id
        context['comment_ctype_id'] = ContentType.objects.get(model='comment').id
        return context

    def get_success_url(self):
        """
        Return the URL to redirect to after a successful comment submission.

        - Redirects back to the current item's detail page.
        """
        return reverse("item-detail", kwargs={"id": self.object.id})

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests (comment submission).

        - Sets self.object to the current PostItem (required for context/form).
        - Validates the form and delegates to form_valid() or form_invalid().
        """
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        """
        Save the comment when the form is valid.

        - Creates a Comment instance but doesn't save to DB yet (commit=False).
        - Assigns the current PostItem and User to the comment.
        - Saves the comment to the database.
        """
        comment = form.save(commit=False)
        comment.post_item = self.object  
        comment.author = self.request.user 
        comment.save() 
        return super().form_valid(form)


class ItemCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    Class-based create view for posting a new item to the market.

    - Requires the user to be logged in (via LoginRequiredMixin).
    - Requires the user to have at least one verified email address 
        (via UserPassesTestMixin + test_func).
    - Uses PostItem as the underlying model.
    - Uses PostItemCreateForm to render and validate the form fields.
    - Renders the 'market/item_form.html' template.
    - Automatically sets the current logged-in user as the item_author.
    - After a successful create, redirects to the item detail page for the new item.
    """

    # The model that will be created when the form is submitted successfully
    model = PostItem

    # The ModelForm used to render and validate input for a new PostItem
    # (create-only fields: does not expose `is_sold`)
    form_class = PostItemCreateForm

    # Template used to render the "create item" form page
    template_name = "market/item_form.html"

    # When the email verification test fails, redirect instead of returning HTTP 403
    redirect_unauthenticated_users = True

    # Custom redirect handler that sends a confirmation email
    # and forwards the user to the "email confirmation required" page
    raise_exception = confirmation_required_redirect

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

    def test_func(self, user):
        """
        Permission check used by UserPassesTestMixin.

        - Returns True only if the given user has a verified email address.
        - If this returns False, the view uses confirmation_required_redirect
            instead of rendering the form.
        """
        return EmailAddress.objects.filter(user=user, verified=True).exists()

class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Class-based update view for editing an existing PostItem.

    - Requires the user to be logged in (via LoginRequiredMixin).
    - Restricts access so that only the original author can edit the item
        (via UserPassesTestMixin + test_func).
    - Uses PostItem as the underlying model.
    - Uses PostItemUpdateForm to render and validate the form fields,
        including the 'is_sold' flag.
    - Renders the same 'market/item_form.html' template as the create view.
    - Retrieves the item to edit based on the 'id' parameter from the URL.
    - After a successful update, redirects to the updated item's detail page.
    """

    # The model instance that will be retrieved and updated
    model = PostItem

    # The ModelForm used to render and validate input for an existing PostItem
    form_class = PostItemUpdateForm

    # Template used to render the "edit item" form page (shared with create view)
    template_name = "market/item_form.html"

    # Name of the URL keyword argument used to look up the object
    pk_url_kwarg = "id"

    # With UserPassesTestMixin: return HTTP 403 instead of redirect when test_func fails
    raise_exception = True

    def get_success_url(self):
        """
        Return the URL to redirect to after successfully updating an item.

        - Redirects to the item detail page using the updated object's ID.
        """
        return reverse("item-detail", kwargs={"id": self.object.id})

    def test_func(self, user):
        """
        Permission check used by UserPassesTestMixin.

        - Allows access only if the current user is the author of the PostItem.
        """
        post_item = self.get_object()
        return post_item.item_author == user


class ItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Class-based delete view for removing an existing PostItem.

    - Requires the user to be logged in (via LoginRequiredMixin).
    - Restricts access so that only the original author can delete the item
        (via UserPassesTestMixin + test_func).
    - Uses PostItem as the underlying model.
    - Renders a confirmation page using 'market/item_confirm_delete.html'.
    - Retrieves the item to delete based on the 'id' parameter from the URL.
    - After successful deletion, redirects back to the home (item list) page.
        cessful deletion, redirects back to the home (item list) page.
    """

    # The model instance that will be retrieved and deleted
    model = PostItem

    # Template used to render the delete confirmation page
    template_name = "market/item_confirm_delete.html"

    # Name of the URL keyword argument used to look up the object to delete
    pk_url_kwarg = "id"

    # With UserPassesTestMixin: return HTTP 403 instead of redirect when test_func fails
    raise_exception = True

    def get_success_url(self):
        """
        Return the URL to redirect to after successfully deleting an item.

        - Redirects to the home page that lists all items.
        """
        return reverse("home")

    def test_func(self, user):
        """
        Permission check used by UserPassesTestMixin.

        - Allows access only if the current user is the author of the PostItem.
        """
        post_item = self.get_object()
        return post_item.item_author == user


class ProfileView(DetailView):
    """
    Class-based detail view for displaying a user's profile page.

    - Uses the custom User model as the underlying model.
    - Renders the 'market/profile.html' template.
    - Exposes the User instance in the template as 'profile_user'.
    - Additionally provides the latest 4 PostItem objects authored by this user.
    """

    # The model that this detail view will retrieve a single instance of
    model = User

    # Template used to render the profile page
    template_name = "market/profile.html"

    # Name of the URL keyword argument used to look up the user
    pk_url_kwarg = "id"

    # Context variable name used in the template for the user instance
    context_object_name = "profile_user"

    def get_context_data(self, **kwargs):
        """
        Extend the default context with the user's recent PostItem listings.

        - Adds 'user_postitems' containing the 4 most recently created posts
            authored by the profile user.
        - Relies on PostItem's default ordering (newest first).
        """
        # Start with the default context provided by DetailView
        context = super().get_context_data(**kwargs)

        # Current profile owner (User instance for this page)
        profile_user = self.object

        # Latest 4 items posted by this user, ordered by creation date (newest first)
        context["user_postitems"] = profile_user.posts.all()[:4]

        return context


class UserPostItemListView(ListView):
    """
    List view for displaying all PostItem objects authored by a specific user.

    - Uses PostItem as the underlying model.
    - Expects a URL kwarg 'id' containing the User primary key.
    - Paginates the result set, showing 8 items per page.
    - Additionally exposes the profile owner as 'profile_user' in the template context
        so the template can render user-specific information (nickname, avatar, etc.).
    - Results are ordered by PostItem.Meta default (newest first).
    """

    # Model that this list view will query
    model = PostItem

    # Template used to render the user's item list
    template_name = "market/user_item_list.html"

    # Context variable name used in the template for the queryset of PostItem objects
    context_object_name = "user_postitems"

    # Number of PostItem objects per page
    paginate_by = 8

    def get_queryset(self):
        """
        Return the queryset of PostItem objects for the given user.

        - Resolves the User instance from the 'id' URL kwarg.
        - Stores the resolved user on 'self.profile_user' for later reuse.
        - Returns all PostItem objects authored by this user, ordered by newest first.
        """
        # Look up the profile owner (User) based on the URL parameter 'id';
        # raise 404 if no such user exists.
        self.profile_user = get_object_or_404(User, pk=self.kwargs.get("id"))

        # Return all posts authored by this user, newest first
        return self.profile_user.posts.all()

    def get_context_data(self, **kwargs):
        """
        Extend the default context with the profile owner.

        - Adds 'profile_user' so the template can access user information
            (nickname, profile picture, etc.) alongside the item list.
        """
        # Start with the default context from ListView (which includes 'user_postitems')
        context = super().get_context_data(**kwargs)

        # Add the current profile owner (User instance) to the context
        context["profile_user"] = self.profile_user

        return context


class ProfileSetView(LoginRequiredMixin, UpdateView):
    """
    View for editing the currently logged-in user's profile.

    - Uses the custom User model as the underlying model.
    - Renders 'market/profile_form.html' with ProfileForm.
    - Always edits request.user (no pk in URL).
    """

    # Underlying model: custom User
    model = User

    # Form used to edit the profile fields
    form_class = ProfileForm

    # Template for the profile edit page
    template_name = "market/profile_set_form.html"

    def get_object(self, queryset=None):
        """
        Always return the currently logged-in user.

        This ensures users can only edit their own profile, even if someone
        tries to guess another user's ID.
        """
        return self.request.user

    def get_success_url(self):
        """
        Where to redirect after a successful profile update.

        - Here we redirect to 'home', but you can change it to 'profile'
            if you want to go back to the profile detail page instead.
        """
        return reverse("home")


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    View for editing the currently logged-in user's profile.

    - Uses the custom User model as the underlying model.
    - Renders 'market/profile_update_form.html' with ProfileForm.
    - Always edits request.user (no pk in URL).
    - After a successful update, redirects to the profile detail page.
    """

    # Underlying model: custom User
    model = User

    # Form used to edit the profile fields
    form_class = ProfileForm

    # Template for the profile edit page
    template_name = "market/profile_update_form.html"

    def get_object(self, queryset=None):
        """
        Always return the currently logged-in user.

        This ensures users can only edit their own profile, even if someone
        tries to guess another user's ID.
        """
        return self.request.user

    def get_success_url(self):
        """
        Where to redirect after a successful profile update.

        - Redirects to the 'profile' detail page of the current user.
        """
        return reverse("profile", kwargs=(({"id": self.request.user.id})))


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    View for updating an existing comment.

    - Uses CommentForm via POST requests (intended for in-place editing).
    - Redirects GET requests to the parent item detail page to prevent standalone access.
    - Requires login and author verification.
    """

    model = Comment
    form_class = CommentForm
    pk_url_kwarg = "comment_id" 

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests by redirecting to the item detail page.

        - Since comment editing happens via a hidden form on the detail page,
            direct access to the edit URL is unnecessary and blocked.
        """
        return redirect("item-detail", id=self.get_object().post_item.id)

    def get_success_url(self):
        """
        Return the URL to redirect to after successful comment update.

        - Redirects back to the related PostItem detail page.
        """
        return reverse("item-detail", kwargs={"id": self.object.post_item.id})

    def test_func(self, user):
        """
        Permission check: Only the author of the comment can update it.
        """
        return self.get_object().author == user


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    View for deleting an existing comment.

    - Handles deletion via POST requests (triggered by a JS modal).
    - Redirects GET requests to the parent item detail page.
    - Requires login and author verification.
    """

    model = Comment
    pk_url_kwarg = "comment_id"

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests by redirecting to the item detail page.

        - Deletion should be performed via POST for security.
        - Direct access to this URL via GET is blocked.
        """
        return redirect("item-detail", id=self.get_object().post_item.id)

    def get_success_url(self):
        """
        Return the URL to redirect to after successful deletion.

        - Redirects back to the related PostItem detail page.
        """
        return reverse("item-detail", kwargs={"id": self.object.post_item.id})

    def test_func(self, user):
        """
        Permission check: Only the author of the comment can delete it.
        """
        return self.get_object().author == user


class ProcessLikeView(LoginRequiredMixin, View):
    """
    Class-based view for handling 'Like' toggles via AJAX POST requests.

    - Requires the user to be logged in (via LoginRequiredMixin).
    - Only accepts POST requests (http_method_name = ["post"]).
    - Toggles the like status: creates a Like if it doesn't exist, deletes it if it does.
    - Returns a JsonResponse with the new like status and total count,
        allowing the frontend to update the UI without a page reload.
    """

    http_method_name = ["post"]

    def post(self, request, *args, **kwargs):
        """
        Handle the POST request to toggle a like.

        - Retrieves the content type and object ID from the URL kwargs.
        - Uses get_or_create to either find an existing like or create a new one.
        - If the like already existed (not created), it is deleted (unlike).
        - Calculates the new total like count for the object.
        - Returns JSON data containing:
            - 'liked': Boolean indicating if the user currently likes the item.
            - 'like_count': The updated total number of likes.
        """
        content_type_id = self.kwargs.get("content_type_id")
        object_id = self.kwargs.get("object_id")

        like, created = Like.objects.get_or_create(
            author=self.request.user,
            content_type_id=self.kwargs.get("content_type_id"),
            object_id=self.kwargs.get("object_id"),
        )

        if not created:
            like.delete()
            liked = False
        else:
            liked = True

        like_count = Like.objects.filter(
            content_type_id=content_type_id, object_id=object_id
        ).count()

        return JsonResponse(
            {
                "liked": liked,
                "like_count": like_count,
            }
        )
