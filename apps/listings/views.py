from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .models import Listing, Category, Application
from .forms import ListingForm


def listing_list(request):
    listings = Listing.objects.select_related("category", "user").order_by("-date_posted")

    # Only accept a numeric category id, so ?category=abc can't crash the page
    selected_category = None
    category_id = request.GET.get("category", "")
    if category_id.isdigit():
        selected_category = int(category_id)
        listings = listings.filter(category_id=selected_category)

    return render(request, "listings/listing_list.html", {
        "listings": listings,
        "categories": Category.objects.all(),
        "selected_category": selected_category,
    })


def listing_detail(request, pk):
    listing = get_object_or_404(
        Listing.objects.select_related("category", "user"), pk=pk
    )

    has_applied = False
    if request.user.is_authenticated:
        has_applied = Application.objects.filter(
            listing=listing, applicant=request.user
        ).exists()

    return render(request, "listings/listing_detail.html", {
        "listing": listing,
        "has_applied": has_applied,
        "is_owner": listing.user_id == request.user.id,
    })


@login_required
@require_POST
def listing_apply(request, pk):
    listing = get_object_or_404(Listing, pk=pk)

    # You can't respond to your own listing, or to one that isn't open
    if listing.user_id != request.user.id and listing.status == "open":
        Application.objects.get_or_create(listing=listing, applicant=request.user)

    return redirect("listings:listing_detail", pk=pk)


@login_required
def listing_create(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.user = request.user
            listing.save()
            return redirect("listings:listing_detail", pk=listing.pk)
    else:
        form = ListingForm()
    return render(request, "listings/listing_form.html", {"form": form})