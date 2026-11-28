from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from .models import UserSettings
from .forms import UserSettingsForm

@login_required
def settings_view(request):
    # Fetch preferences, or create defaults if they just registered
    user_settings, created = UserSettings.objects.get_or_create(user=request.user)

    form = UserSettingsForm(instance=user_settings)
    password_form = PasswordChangeForm(request.user)

    if request.method == "POST":
        if "change_password" in request.POST:
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                # Keep the person logged in after the password changes
                update_session_auth_hash(request, user)
                messages.success(request, "Your password was changed.")
                return redirect("user_settings:settings")
        else:
            form = UserSettingsForm(request.POST, instance=user_settings)
            if form.is_valid():
                form.save()
                messages.success(request, "Settings saved.")
                return redirect("user_settings:settings")

    return render(request, "user_settings/settings.html", {
        "form": form,
        "password_form": password_form,
        "settings": user_settings,
    })
