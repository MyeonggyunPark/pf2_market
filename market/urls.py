from django.urls import path
from . import views


# URL configuration for the market app
urlpatterns = [

    # Home page: shows the list of all items using IndexView
    path("", views.IndexView.as_view(), name="home"),

    # Detail page: shows a single item by its ID using ItemDetailView
    path("detail/<int:id>/", views.ItemDetailView.as_view(), name="item-detail"),
]
