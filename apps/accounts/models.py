from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Maps to the ERD's User entity.
    username, password, email, date_joined are already provided by AbstractUser —
    don't redeclare them.
    """
    full_name = models.CharField(max_length=150)
    age = models.PositiveIntegerField(null=True, blank=True)
    contact_number = models.CharField(max_length=20, blank=True)
    barangay = models.CharField(max_length=100)
    address = models.CharField(max_length=255, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Admin(models.Model):
    """
    Maps to the ERD's Admin entity. Deliberately NOT related to User —
    barangay admins who moderate listings are a separate account type.
    """
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    contact_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField()

    def __str__(self):
        return self.username