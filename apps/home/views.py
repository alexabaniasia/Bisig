from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.listings.models import Category, Listing


@login_required
def home_view(request):
    return render(request, "home/home.html", {
        "categories": Category.objects.order_by("category_name")[:6],
        "recent_listings": (
            Listing.objects.select_related("category", "user")
            .filter(status="open")
            .order_by("-date_posted")[:5]
        ),
    })