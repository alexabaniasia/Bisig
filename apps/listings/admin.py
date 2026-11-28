from django.contrib import admin

from .models import Application, Category, Listing, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("category_name",)
    search_fields = ("category_name",)


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "category", "listing_type", "status", "date_posted")
    list_filter = ("status", "listing_type", "category")
    search_fields = ("title", "description", "user__username")


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("listing", "applicant", "status", "date_applied")
    list_filter = ("status",)
    search_fields = ("listing__title", "applicant__username")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("reviewer", "reviewee", "rating", "date_reviewed")
    list_filter = ("rating",)
    search_fields = ("reviewer__username", "reviewee__username", "comment")
