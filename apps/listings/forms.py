from django import forms
from .models import Listing

class ListingForm(forms.ModelForm):
    LISTING_TYPE_CHOICES = [
        ("offer", "I'm offering this skill"),
        ("request", "I need help with this"),
    ]

    listing_type = forms.ChoiceField(choices=LISTING_TYPE_CHOICES)

    class Meta:
        model = Listing
        fields = ["category", "title", "description", "listing_type"]