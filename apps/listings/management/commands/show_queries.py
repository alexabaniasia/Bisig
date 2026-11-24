from django.core.management.base import BaseCommand

from apps.listings.models import Listing, Category, Application
from apps.listings.queries import listings_with_category_and_user, requests_needing_help


class Command(BaseCommand):
    help = "Print the SQL that Django generates for the JOIN and SUBQUERY features"

    def handle(self, *args, **options):
        user_model = Listing._meta.get_field("user").related_model

        self.stdout.write("TABLES")
        for model in (Listing, Category, Application, user_model):
            self.stdout.write(f"  {model.__name__}: {model._meta.db_table}")

        join_qs = listings_with_category_and_user()
        self.stdout.write("\n=== JOIN: listings + category + user ===")
        self.stdout.write(str(join_qs.query))
        self.stdout.write(f"Rows returned: {join_qs.count()}")

        sub_qs = requests_needing_help()
        self.stdout.write("\n=== SUBQUERY: requests with no responses ===")
        self.stdout.write(str(sub_qs.query))
        self.stdout.write(f"Rows returned: {sub_qs.count()}")