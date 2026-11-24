from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.core.exceptions import PermissionDenied
from .models import Listing, Category, Application
from .forms import ListingForm
from django.db.models import Count, Q
from django.core.paginator import Paginator
from .queries import listings_with_category_and_user, requests_needing_help

def listing_list(request):
    listings = listings_with_category_and_user()

    # Only accept a numeric category id, so ?category=abc can't crash the page
    selected_category = None
    category_id = request.GET.get("category", "")
    if category_id.isdigit():
        selected_category = int(category_id)
        listings = listings.filter(category_id=selected_category)

    paginator = Paginator(listings, 9)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(request, "listings/listing_list.html", {
        "listings": page_obj,
        "page_obj": page_obj,
        "categories": Category.objects.all(),
        "selected_category": selected_category,
    })


def listing_detail(request, pk):
    listing = get_object_or_404(
        Listing.objects.select_related("category", "user"), pk=pk
    )
    is_owner = listing.user_id == request.user.id

    my_application = None
    applications = None
    if request.user.is_authenticated:
        if is_owner:
            applications = (
                listing.applications.select_related("applicant")
                .order_by("-date_applied")
            )
        else:
            my_application = Application.objects.filter(
                listing=listing, applicant=request.user
            ).first()

    return render(request, "listings/listing_detail.html", {
        "listing": listing,
        "is_owner": is_owner,
        "my_application": my_application,
        "has_applied": my_application is not None,
        "applications": applications,
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

@login_required
@require_POST
def application_update(request, pk):
    application = get_object_or_404(
        Application.objects.select_related("listing"), pk=pk
    )
    # Only the person who posted the listing can accept or decline
    if application.listing.user_id != request.user.id:
        raise PermissionDenied

    action = request.POST.get("action")
    if action == "accept":
        application.status = "accepted"
    elif action == "reject":
        application.status = "rejected"
    else:
        return redirect("listings:listing_detail", pk=application.listing_id)

    application.save(update_fields=["status"])
    return redirect("listings:listing_detail", pk=application.listing_id)


@login_required
@require_POST
def listing_set_status(request, pk):
    # Non-owners get a 404 here
    listing = get_object_or_404(Listing, pk=pk, user=request.user)
    new_status = request.POST.get("status")
    if new_status in ("open", "closed"):
        listing.status = new_status
        listing.save(update_fields=["status"])
    return redirect("listings:listing_detail", pk=pk)

@login_required
def my_activity(request):
    my_listings = (
        Listing.objects.filter(user=request.user)
        .select_related("category")
        .annotate(
            response_count=Count("applications"),
            pending_count=Count("applications", filter=Q(applications__status="pending")),
        )
        .order_by("-date_posted")
    )
    my_applications = (
        Application.objects.filter(applicant=request.user)
        .select_related("listing", "listing__user")
        .order_by("-date_applied")
    )
    return render(request, "listings/my_activity.html", {
        "my_listings": my_listings,
        "my_applications": my_applications,
    })

@login_required
def listing_edit(request, pk):
    # Non-owners get a 404
    listing = get_object_or_404(Listing, pk=pk, user=request.user)
    if request.method == "POST":
        form = ListingForm(request.POST, instance=listing)
        if form.is_valid():
            form.save()
            return redirect("listings:listing_detail", pk=listing.pk)
    else:
        form = ListingForm(instance=listing)
    return render(request, "listings/listing_form.html", {"form": form, "listing": listing})


@login_required
@require_POST
def listing_delete(request, pk):
    listing = get_object_or_404(Listing, pk=pk, user=request.user)
    listing.delete()
    return redirect("listings:my_activity")

def needs_help(request):
    return render(request, "listings/needs_help.html", {
        "listings": requests_needing_help(),
    })