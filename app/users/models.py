from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Future-proof custom user model (start simple, add fields later)"""

    # For MVP: Just use standard Django User fields
    # Later: Add user_type, department, etc. as needed
    is_se_team = models.BooleanField(default=False)

    class Meta:
        db_table = "users"
