from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom user model for Kosmos ERP.
    """
    is_logistics_admin = models.BooleanField(default=False)
    # Add other role-based fields here if necessary
    
    def __str__(self):
        return self.username
