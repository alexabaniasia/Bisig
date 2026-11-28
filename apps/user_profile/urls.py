from django.urls import path
from .views import profile_view, public_profile_view

app_name = "user_profile"
urlpatterns = [
    path("", profile_view, name="profile"),
    path("<str:username>/", public_profile_view, name="public_profile"),
]
