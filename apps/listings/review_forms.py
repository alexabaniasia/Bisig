from django import forms

from .models import Review


class ReviewForm(forms.ModelForm):
    # Shown as clickable stars; 5 first so the CSS can highlight stars to the left
    rating = forms.TypedChoiceField(
        choices=[(5, "5"), (4, "4"), (3, "3"), (2, "2"), (1, "1")],
        coerce=int,
        widget=forms.RadioSelect,
        error_messages={"required": "Please pick a star rating."},
    )
    comment = forms.CharField(
        required=False,
        max_length=500,
        widget=forms.Textarea(attrs={
            "rows": 4,
            "maxlength": 500,
            "placeholder": "How did it go? (optional)",
        }),
    )

    class Meta:
        model = Review
        fields = ["rating", "comment"]
