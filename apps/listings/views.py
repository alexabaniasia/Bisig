from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Listing, Category
from .forms import ListingForm


def listing_list(request):
    listings = Listing.objects.select_related("category", "user").order_by("-date_posted")

    category_id = request.GET.get("category")
    if category_id:
        listings = listings.filter(category_id=category_id)

    return render(request, "listings/listing_list.html", {
        "listings": listings,
        "categories": Category.objects.all(),
        "selected_category": int(category_id) if category_id else None,
    })


@login_required
def listing_create(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.user = request.user
            listing.save()
            return redirect("listings:listing_list")
    else:
        form = ListingForm()
    return render(request, "listings/listing_form.html", {"form": form})