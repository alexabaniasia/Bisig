from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import UserProfile
from .forms import UserProfileForm

@login_required
def profile_view(request):
    # Fetch the user's profile, or create a blank one if they just registered
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        # request.FILES is required whenever you are uploading images/files
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("user_profile:profile")
    else:
        form = UserProfileForm(instance=profile)

    return render(request, "user_profile/profile.html", {
        "form": form,
        "profile": profile
    })