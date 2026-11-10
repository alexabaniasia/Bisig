from django.conf import settings
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(
        upload_to="user_profile/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.user.username