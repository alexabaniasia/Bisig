from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404, redirect, render

from apps.listings.models import Listing, Review
from apps.user_settings.models import UserSettings

from .forms import UserDetailsForm, UserProfileForm
from .models import UserProfile

User = get_user_model()


@login_required
def profile_view(request):
    # Fetch the user's profile, or create a blank one if they just registered
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        # request.FILES is required whenever you are uploading images/files
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        details_form = UserDetailsForm(request.POST, instance=request.user)
        # Check both forms so every error is shown at once
        if all([form.is_valid(), details_form.is_valid()]):
            form.save()
            details_form.save()
            messages.success(request, "Your profile was updated.")
            return redirect("user_profile:profile")
    else:
        form = UserProfileForm(instance=profile)
        details_form = UserDetailsForm(instance=request.user)

    return render(request, "user_profile/profile.html", {
        "form": form,
        "details_form": details_form,
        "profile": profile,
    })


@login_required
def public_profile_view(request, username):
    member = get_object_or_404(User, username=username)
    profile = UserProfile.objects.filter(user=member).first()
    prefs = UserSettings.objects.filter(user=member).first()

    # Contact number is only shown if the member chose to share it in Settings
    show_contact = bool(prefs and prefs.show_contact_number and member.contact_number)

    received = Review.objects.filter(reviewee=member)
    stats = received.aggregate(avg=Avg("rating"), count=Count("id"))
    average = round(stats["avg"], 1) if stats["avg"] else None

    reviews = (
        received.select_related("reviewer", "application__listing")
        .order_by("-date_reviewed")[:20]
    )
    listings = (
        Listing.objects.filter(user=member, status="open")
        .select_related("category")
        .order_by("-date_posted")
    )

    return render(request, "user_profile/public_profile.html", {
        "member": member,
        "profile": profile,
        "show_contact": show_contact,
        "average": average,
        "average_stars": int(round(stats["avg"])) if stats["avg"] else 0,
        "review_count": stats["count"],
        "reviews": reviews,
        "listings": listings,
        "is_me": member.id == request.user.id,
    })
