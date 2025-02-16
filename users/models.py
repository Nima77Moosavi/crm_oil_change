from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('The phone number must be set')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)  # Hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone_number, password, **extra_fields)

class CustomUser(AbstractUser):
    # Remove the default username field
    username = None
    # Add phone number as the unique identifier
    phone_number = models.CharField(_('phone number'), max_length=15, unique=True)
    address = models.TextField(blank=True, null=True)

    # Set the USERNAME_FIELD to phone_number
    USERNAME_FIELD = 'phone_number'
    # No additional required fields for createsuperuser
    REQUIRED_FIELDS = []

    # Use the custom user manager
    objects = CustomUserManager()

    def __str__(self):
        return self.phone_number