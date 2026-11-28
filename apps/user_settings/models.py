from django.conf import settings
from django.db import models

class UserSettings(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    dark_mode = models.BooleanField(default=False)
    # Kept for compatibility; email notifications are not part of the app
    email_notifications = models.BooleanField(default=True)
    # Privacy: show my contact number on my public profile
    show_contact_number = models.BooleanField(default=False)

    def __str__(self):
        return f"Settings for {self.user.username}"
