import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from users.managers import UserManager

class User(AbstractUser, PermissionsMixin):
    username = None  # Remove username field
    id = models.BigAutoField(primary_key=True, editable=False)
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    first_name = models.CharField(verbose_name=_("First Name"), max_length=80)
    last_name = models.CharField(verbose_name=_("Last Name"), max_length=80)
    email = models.EmailField(
        verbose_name=_("Email Address"), unique=True, db_index=True
    )
   
    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ["-date_joined"]
        db_table = 'users'

    @property
    def get_full_name(self) -> str:
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()
