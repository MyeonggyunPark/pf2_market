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
]
