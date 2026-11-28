from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.listings.models import Application, Category, Listing

User = get_user_model()

# (username, full name, barangay)
USERS = [
    ("demo_ana", "Ana Reyes", "Lahug"),
    ("demo_ben", "Ben Cruz", "Mabolo"),
    ("demo_carla", "Carla Santos", "Guadalupe"),
    ("demo_dino", "Dino Villanueva", "Banilad"),
    ("demo_elena", "Elena Garcia", "Talamban"),
]

CATEGORIES = [
    "Tutoring", "Plumbing", "Cooking", "Gardening",
    "Errands", "Repairs", "Childcare", "Tech Help",
]

# (key, owner, category, type, status, title, description)
LISTINGS = [
    ("math_tutor", "demo_ana", "Tutoring", "offer", "open",
     "Math and Science tutoring for grade school",
     "I can help Grade 3 to 6 students with homework and exam review. Weekday afternoons, at my house or yours."),
    ("faucet_repair", "demo_ben", "Plumbing", "offer", "open",
     "Leaky faucet and pipe repair",
     "Experienced with faucets, toilet flush systems and minor pipe leaks. I bring my own tools. Fair rates for neighbors."),
    ("home_cooking", "demo_carla", "Cooking", "offer", "open",
     "Home-cooked meals for small gatherings",
     "I cook Filipino dishes like adobo, kare-kare and pancit for up to 20 people. Please order 2 days in advance."),
    ("garden_care", "demo_dino", "Gardening", "offer", "open",
     "Garden clean-up and plant care",
     "Grass cutting, pruning and planting. I can also give advice on starting a small vegetable garden."),
    ("tech_help", "demo_elena", "Tech Help", "offer", "open",
     "Phone and laptop troubleshooting",
     "Slow phone, forgotten password or Wi-Fi problems? I can help seniors and beginners."),
    ("babysit_offer", "demo_ana", "Childcare", "offer", "closed",
     "After-school babysitting",
     "Available Monday to Friday, 3 to 6 PM. Currently fully booked."),
    ("fan_repair", "demo_ben", "Repairs", "offer", "open",
     "Electric fan and small appliance repair",
     "I can fix electric fans, rice cookers and irons. Bring it over and I will quote you a price."),
    ("english_tutor", "demo_carla", "Tutoring", "request", "open",
     "Need an English tutor for my 10-year-old",
     "Looking for someone patient to help with reading and grammar twice a week."),
    ("clogged_sink", "demo_dino", "Plumbing", "request", "open",
     "Clogged kitchen sink needs fixing",
     "Water drains very slowly. Looking for a neighbor who can unclog it this weekend."),
    ("groceries", "demo_elena", "Errands", "request", "open",
     "Someone to buy groceries on Saturday",
     "I have a sprained ankle and need help with a small grocery list from the nearby market."),
    ("veggie_garden", "demo_ana", "Gardening", "request", "open",
     "Help planting a small vegetable garden",
     "I have a small backyard and need guidance on what to plant and how to prepare the soil."),
    ("birthday_cook", "demo_ben", "Cooking", "request", "pending",
     "Cook needed for a birthday party",
     "I need 30 servings of pancit and lumpia on December 20."),
    ("wifi_router", "demo_carla", "Tech Help", "request", "open",
     "Help setting up a Wi-Fi router",
     "My new router is still in the box and I do not know how to set it up."),
    ("door_hinge", "demo_dino", "Repairs", "request", "open",
     "Door hinge needs repair",
     "The front door is sagging and hard to close. I need someone with basic carpentry skills."),
    ("babysit_request", "demo_elena", "Childcare", "request", "closed",
     "Looking for a weekend babysitter",
     "Resolved, thank you neighbors!"),
]

# (listing key, applicant, status)
APPLICATIONS = [
    ("math_tutor", "demo_carla", "pending"),
    ("faucet_repair", "demo_dino", "accepted"),
    ("tech_help", "demo_ana", "rejected"),
    ("english_tutor", "demo_ana", "pending"),
    ("english_tutor", "demo_elena", "pending"),
    ("clogged_sink", "demo_ben", "pending"),
    ("veggie_garden", "demo_dino", "accepted"),
    ("birthday_cook", "demo_carla", "accepted"),
    ("babysit_request", "demo_ana", "accepted"),
]


class Command(BaseCommand):
    help = "Add (or remove with --clear) demo users, listings and responses"

    def add_arguments(self, parser):
        parser.add_argument("--password", default="DemoPass2026!",
                            help="Password for the demo accounts")
        parser.add_argument("--clear", action="store_true",
                            help="Delete the demo users and everything they own")

    @transaction.atomic
    def handle(self, *args, **options):
        usernames = [u[0] for u in USERS]

        if options["clear"]:
            deleted, _ = User.objects.filter(username__in=usernames).delete()
            self.stdout.write(f"Removed demo users and their data ({deleted} rows).")
            return

        categories = {}
        for name in CATEGORIES:
            category = (Category.objects.filter(category_name=name).first()
                        or Category.objects.create(category_name=name))
            categories[name] = category

        users = {}
        for username, full_name, barangay in USERS:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={"full_name": full_name, "barangay": barangay, "is_verified": True},
            )
            if created:
                user.set_password(options["password"])
                user.save()
            users[username] = user

        listings = {}
        new_listings = 0
        for key, owner, category, ltype, status, title, description in LISTINGS:
            listing = Listing.objects.filter(user=users[owner], title=title).first()
            if listing is None:
                listing = Listing.objects.create(
                    user=users[owner], category=categories[category], title=title,
                    description=description, listing_type=ltype, status=status,
                )
                new_listings += 1
            listings[key] = listing

        new_apps = 0
        for key, applicant, status in APPLICATIONS:
            _, created = Application.objects.get_or_create(
                listing=listings[key], applicant=users[applicant],
                defaults={"status": status},
            )
            new_apps += int(created)

        self.stdout.write(self.style.SUCCESS(
            f"Done. Added {new_listings} listings and {new_apps} responses."))
        self.stdout.write("Demo logins: " + ", ".join(usernames))
        self.stdout.write(f"Password: {options['password']}")