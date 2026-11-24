from django.urls import path
from . import views

app_name = "listings"
urlpatterns = [
    path("", views.listing_list, name="listing_list"),
    path("new/", views.listing_create, name="listing_create"),
    path("<int:pk>/", views.listing_detail, name="listing_detail"),
    path("<int:pk>/apply/", views.listing_apply, name="listing_apply"),
    path("applications/<int:pk>/update/", views.application_update, name="application_update"),
    path("<int:pk>/status/", views.listing_set_status, name="listing_set_status"),
    path("mine/", views.my_activity, name="my_activity"),
]