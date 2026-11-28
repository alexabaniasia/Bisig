from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ListingForm
from .models import Application, Category, Listing, Review
from .queries import (
    filter_listings,
    listings_with_category_and_user,
    requests_needing_help,
)
from .review_forms import ReviewForm

SORT_OPTIONS = [("new", "Newest first"), ("old", "Oldest first"), ("title", "Title A-Z")]
TYPE_OPTIONS = [("", "Offers & requests"), ("offer", "Offers only"), ("request", "Requests only")]


def _query_string(params, **overrides):
    """Build a '?a=1&b=2' string from the active filters, with some values replaced."""
    merged = {**params, **overrides}
    merged = {k: v for k, v in merged.items() if v not in (None, "")}
    return "?" + urlencode(merged) if merged else "?"


def listing_list(request):
    q = request.GET.get("q", "").strip()[:100]

    listing_type = request.GET.get("type", "")
    if listing_type not in ("offer", "request"):
        listing_type = ""

    sort = request.GET.get("sort", "new")
    if sort not in dict(SORT_OPTIONS):
        sort = "new"

    # Only accept a numeric category id, so ?category=abc can't crash the page
    category_param = request.GET.get("category", "")
    selected_category = int(category_param) if category_param.isdigit() else None

    listings = filter_listings(
        listings_with_category_and_user(),
        q=q, listing_type=listing_type, category_id=selected_category, sort=sort,
    )

    params = {
        "q": q,
        "type": listing_type,
        "sort": "" if sort == "new" else sort,
        "category": selected_category,
    }

    paginator = Paginator(listings, 9)
    page_obj = paginator.get_page(request.GET.get("page"))

    category_chips = [{
        "name": "All",
        "url": _query_string(params, category=None),
        "active": selected_category is None,
    }]
    for category in Category.objects.order_by("category_name"):
        category_chips.append({
            "name": category.category_name,
            "url": _query_string(params, category=category.id),
            "active": selected_category == category.id,
        })

    return render(request, "listings/listing_list.html", {
        "listings": page_obj,
        "page_obj": page_obj,
        "total": paginator.count,
        "category_chips": category_chips,
        "selected_category": selected_category,
        "q": q,
        "listing_type": listing_type,
        "sort": sort,
        "sort_options": SORT_OPTIONS,
        "type_options": TYPE_OPTIONS,
        "filters_active": bool(q or listing_type or selected_category or sort != "new"),
        "prev_url": _query_string(params, page=page_obj.previous_page_number()) if page_obj.has_previous() else "",
        "next_url": _query_string(params, page=page_obj.next_page_number()) if page_obj.has_next() else "",
    })


def listing_detail(request, pk):
    listing = get_object_or_404(
        Listing.objects.select_related("category", "user"), pk=pk
    )
    is_owner = listing.user_id == request.user.id

    my_application = None
    applications = None
    i_reviewed_owner = False

    if request.user.is_authenticated:
        if is_owner:
            applications = list(
                listing.applications.select_related("applicant").order_by("-date_applied")
            )
            reviewed_ids = set(
                Review.objects.filter(reviewer=request.user, application__in=applications)
                .values_list("application_id", flat=True)
            )
            for application in applications:
                application.i_reviewed = application.id in reviewed_ids
        else:
            my_application = Application.objects.filter(
                listing=listing, applicant=request.user
            ).first()
            if my_application is not None:
                i_reviewed_owner = Review.objects.filter(
                    application=my_application, reviewer=request.user
                ).exists()

    return render(request, "listings/listing_detail.html", {
        "listing": listing,
        "is_owner": is_owner,
        "my_application": my_application,
        "has_applied": my_application is not None,
        "i_reviewed_owner": i_reviewed_owner,
        "applications": applications,
    })


@login_required
@require_POST
def listing_apply(request, pk):
    listing = get_object_or_404(Listing, pk=pk)

    if listing.user_id == request.user.id:
        messages.error(request, "You can't respond to your own listing.")
    elif listing.status != "open":
        messages.error(request, "This listing isn't accepting responses.")
    else:
        _, created = Application.objects.get_or_create(
            listing=listing, applicant=request.user
        )
        if created:
            messages.success(request, f"Your response was sent to {listing.user.username}.")

    return redirect("listings:listing_detail", pk=pk)


@login_required
@require_POST
def application_update(request, pk):
    application = get_object_or_404(
        Application.objects.select_related("listing", "applicant"), pk=pk
    )
    # Only the person who posted the listing can accept or decline
    if application.listing.user_id != request.user.id:
        raise PermissionDenied

    action = request.POST.get("action")
    if action == "accept":
        application.status = "accepted"
        messages.success(request, f"You accepted {application.applicant.username}'s response.")
    elif action == "reject":
        application.status = "rejected"
        messages.info(request, f"You declined {application.applicant.username}'s response.")
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
        messages.success(
            request,
            "Listing reopened." if new_status == "open" else "Listing marked as closed.",
        )
    return redirect("listings:listing_detail", pk=pk)


@login_required
def listing_create(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.user = request.user
            listing.save()
            messages.success(request, "Your listing is now live.")
            return redirect("listings:listing_detail", pk=listing.pk)
    else:
        form = ListingForm()
    return render(request, "listings/listing_form.html", {"form": form})


@login_required
def listing_edit(request, pk):
    # Non-owners get a 404
    listing = get_object_or_404(Listing, pk=pk, user=request.user)
    if request.method == "POST":
        form = ListingForm(request.POST, instance=listing)
        if form.is_valid():
            form.save()
            messages.success(request, "Listing updated.")
            return redirect("listings:listing_detail", pk=listing.pk)
    else:
        form = ListingForm(instance=listing)
    return render(request, "listings/listing_form.html", {"form": form, "listing": listing})


@login_required
@require_POST
def listing_delete(request, pk):
    listing = get_object_or_404(Listing, pk=pk, user=request.user)
    listing.delete()
    messages.success(request, "Listing deleted.")
    return redirect("listings:my_activity")


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


def needs_help(request):
    return render(request, "listings/needs_help.html", {
        "listings": requests_needing_help(),
    })


@login_required
def review_create(request, pk):
    """Either side of an accepted response can review the other, once."""
    application = get_object_or_404(
        Application.objects.select_related("listing", "listing__user", "applicant"),
        pk=pk,
    )
    listing = application.listing

    if request.user.id == listing.user_id:
        reviewee = application.applicant
    elif request.user.id == application.applicant_id:
        reviewee = listing.user
    else:
        raise PermissionDenied

    if application.status != "accepted":
        messages.error(request, "You can review someone after their response has been accepted.")
        return redirect("listings:listing_detail", pk=listing.pk)

    if Review.objects.filter(application=application, reviewer=request.user).exists():
        messages.info(request, "You already reviewed this exchange.")
        return redirect("listings:listing_detail", pk=listing.pk)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.application = application
            review.reviewer = request.user
            review.reviewee = reviewee
            review.save()
            messages.success(request, f"Thanks! Your review for {reviewee.username} was saved.")
            return redirect("listings:listing_detail", pk=listing.pk)
    else:
        form = ReviewForm()

    return render(request, "listings/review_form.html", {
        "form": form,
        "listing": listing,
        "reviewee": reviewee,
    })
