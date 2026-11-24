from django.db.models import Subquery

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