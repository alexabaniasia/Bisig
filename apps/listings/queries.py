from django.db.models import Q, Subquery

from .models import Listing, Application


def listings_with_category_and_user():
    """JOIN: listings + category + user (select_related becomes INNER JOINs)."""
    return (
        Listing.objects.select_related("category", "user")
        .order_by("-date_posted")
    )


def requests_needing_help():
    """SUBQUERY: open requests whose id is NOT in the applications table."""
    responded_listing_ids = Application.objects.values("listing_id")  # inner query
    return (
        Listing.objects.filter(listing_type="request", status="open")  # outer query
        .exclude(id__in=Subquery(responded_listing_ids))
        .select_related("category", "user")
        .order_by("-date_posted")
    )


SORT_FIELDS = {"new": "-date_posted", "old": "date_posted", "title": "title"}


def filter_listings(queryset, q="", listing_type="", category_id=None, sort="new"):
    """Search, filter and sort a listings queryset (used by the Browse page)."""
    for term in q.split():
        queryset = queryset.filter(
            Q(title__icontains=term)
            | Q(description__icontains=term)
            | Q(category__category_name__icontains=term)
            | Q(user__username__icontains=term)
        )
    if listing_type in ("offer", "request"):
        queryset = queryset.filter(listing_type=listing_type)
    if category_id:
        queryset = queryset.filter(category_id=category_id)
    return queryset.order_by(SORT_FIELDS.get(sort, "-date_posted"))
