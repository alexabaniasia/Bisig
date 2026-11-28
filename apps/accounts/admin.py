from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

try:  # Django 5.1+
    from django.contrib.auth.forms import AdminUserCreationForm as BaseCreationForm
except ImportError:  # older Django
    from django.contrib.auth.forms import UserCreationForm as BaseCreationForm

from .models import User


class BisigUserCreationForm(BaseCreationForm):
    class Meta(BaseCreationForm.Meta):
        model = User
        fields = ("username", "full_name", "barangay")


class BisigUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


@admin.register(User)
class BisigUserAdmin(UserAdmin):
    form = BisigUserChangeForm
    add_form = BisigUserCreationForm

    list_display = ("username", "full_name", "barangay", "is_verified", "is_staff")
    list_filter = ("is_verified", "barangay", "is_staff")
    search_fields = ("username", "full_name", "barangay", "email")

    fieldsets = UserAdmin.fieldsets + (
        ("Bisig profile", {"fields": ("full_name", "age", "contact_number", "barangay", "address", "is_verified")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Bisig profile", {"fields": ("full_name", "barangay")}),
    )
