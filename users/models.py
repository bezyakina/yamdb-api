from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole(models.TextChoices):
    """Роли пользователей."""

    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"


class User(AbstractUser):
    """Расширение стандартной модели пользователя Django."""

    bio = models.TextField(blank=True, null=True)
    email = models.EmailField(max_length=255, blank=False, unique=True)
    role = models.CharField(
        max_length=150,
        blank=False,
        choices=UserRole.choices,
        default=UserRole.USER,
    )
    username = models.CharField(
        max_length=255, blank=True, null=True, unique=True, db_index=True
    )
    confirmation_code = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )
    password = models.CharField(max_length=255, blank=False, null=True)

    date_joined = models.DateTimeField(blank=True, null=True)

    first_name = models.TextField(max_length=255, blank=True, null=True)
    last_name = models.TextField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = "users"

    @property
    def is_admin(self):
        return self.role == "admin" or self.is_staff

    @property
    def is_moderator(self):
        return self.role == "moderator"
