from django.urls import path
from . import views


# URL configuration for the market app
urlpatterns = [
    
    # ==========  Urls about PostItem ==========

    # Home page: shows the list of all items using IndexView
    path("", views.IndexView.as_view(), name="home"),
    
    # Detail page: shows a single item by its ID using ItemDetailView
    path("item/<int:id>/", views.ItemDetailView.as_view(), name="item-detail"),

    # Create page: shows a form to create a new item using ItemCreateView
    path("item/create/", views.ItemCreateView.as_view(), name="item-create"),

    # Update page: shows a form to edit an existing item using ItemUpdateView
    path("item/<int:id>/edit/", views.ItemUpdateView.as_view(), name="item-update"),
    
    # Delete page: handles deleting an existing item using ItemDeleteView
    path("item/<int:id>/delete/", views.ItemDeleteView.as_view(), name="item-delete"),



    # ========== Urls about Profile ==========

    # Profile page: shows a user's profile by their ID using ProfileView
    path("users/<int:id>/", views.ProfileView.as_view(), name="profile"),

    # User's items page: shows a paginated list of all items posted by a specific user
    path("user/<int:id>/items/", views.UserPostItemListView.as_view(), name="user-item-list"),
    
    # Profile settings page: allows the currently logged-in user to edit their profile using ProfileSetView
    path("set-profile/", views.ProfileSetView.as_view(), name="profile-set"),
    
    # Profile update page: allows the currently logged-in user to update their existing profile using ProfileUpdateView
    path("update-profile/", views.ProfileUpdateView.as_view(), name="profile-update"),
    

    # ========== Urls about Comment ==========
    
    # Comment update: handles updating an existing comment using CommentUpdateView
    path("comment/<int:comment_id>/edit/", views.CommentUpdateView.as_view(), name="comment-update"),

    # Comment delete: handles deleting an existing comment using CommentDeleteView
    path("comment/<int:comment_id>/delete/", views.CommentDeleteView.as_view(), name="comment-delete"),
    
    
    # ========== Urls about Like ==========
    
    # Process like: handles toggling a like via AJAX POST request using ProcessLikeView
    path("like/<int:content_type_id>/<int:object_id>/", views.ProcessLikeView.as_view(), name="process-like"),
]
