from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('USER', 'User'),
        ('ADMIN', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='USER')

    def save(self, *args, **kwargs):
        if self.is_superuser or self.is_staff:
            self.role = 'ADMIN'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.role})"
