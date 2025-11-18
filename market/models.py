from django.db import models

# Reusable base class for a fully featured User model
from django.contrib.auth.models import AbstractUser


# Custom user model extending Django's default AbstractUser
class User(AbstractUser):

    # Custom optional unique nickname field for each user
    nickname = models.CharField(max_length=15, unique=True, null=True)

    def __str__(self):
        return self.email
