from django import forms
from django.contrib.auth import get_user_model

from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_image']


class UserDetailsForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['full_name', 'barangay', 'contact_number', 'email', 'age', 'address']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Your full name'}),
            'barangay': forms.TextInput(attrs={'placeholder': 'e.g. Lahug'}),
            'contact_number': forms.TextInput(attrs={'placeholder': 'e.g. 0917 123 4567'}),
            'email': forms.EmailInput(attrs={'placeholder': 'you@example.com'}),
            'age': forms.NumberInput(attrs={'min': 13, 'max': 120}),
            'address': forms.TextInput(attrs={'placeholder': 'Street, house number'}),
        }

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is not None and not 13 <= age <= 120:
            raise forms.ValidationError('Please enter an age between 13 and 120.')
        return age
