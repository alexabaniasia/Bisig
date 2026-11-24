from django.db import migrations

CATEGORIES = [
    "Tutoring",
    "Plumbing",
    "Cooking",
    "Gardening",
    "Errands",
    "Repairs",
    "Childcare",
    "Tech Help",
]


def seed_categories(apps, schema_editor):
    Category = apps.get_model("listings", "Category")
    for name in CATEGORIES:
        Category.objects.get_or_create(category_name=name)


class Migration(migrations.Migration):

    dependencies = [
        ("listings", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_categories, migrations.RunPython.noop),
    ]