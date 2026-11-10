from django.conf import settings
from django.db import models

from apps.accounts.models import Admin


class Category(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name


class Listing(models.Model):
    STATUS_CHOICES = [
        ("open", "Open"),
        ("closed", "Closed"),
        ("pending", "Pending"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="listings"
    )
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="listings"
    )
    admin = models.ForeignKey(
        Admin, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="moderated_listings",
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    listing_type = models.CharField(max_length=50)  # e.g. "offer" or "request"
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="open")
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Application(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    ]

    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="applications"
    )
    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applications"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    date_applied = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.applicant} → {self.listing}"


class Review(models.Model):
    application = models.ForeignKey(
        Application, on_delete=models.CASCADE, related_name="reviews"
    )
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews_written"
    )
    reviewee = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews_received"
    )
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    date_reviewed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rating}★ by {self.reviewer} for {self.reviewee}"