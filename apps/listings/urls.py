from django.urls import path
from . import views

app_name = "listings"
urlpatterns = [
    path("", views.listing_list, name="listing_list"),
    path("new/", views.listing_create, name="listing_create"),
]