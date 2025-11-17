from django.db import models

# Reusable base class for a fully featured User model
from django.contrib.auth.models import AbstractUser



# Custom user model extending Django's default AbstractUser
class User(AbstractUser):
    pass
