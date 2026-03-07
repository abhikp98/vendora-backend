from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', User.ADMIN)
        return self.create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    CUSTOMER = 'customer'
    VENDOR = 'vendor'
    ADMIN = 'admin'

    ROLE_CHOICES = [
        (CUSTOMER, 'customer'),
        (VENDOR, 'vendor'),
        (ADMIN, 'admin'),

    ]

    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default=CUSTOMER)
    phone = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(
        upload_to='profiles/', blank=True, null=True)

    objects = UserManager()

    def is_vendor(self):
        return self.role == self.VENDOR

    def is_customer(self):
        return self.role == self.CUSTOMER

    def is_admin(self):
        return self.role == self.ADMIN

    def __str__(self):
        return f"{self.username}, {self.role}"
