from datetime import timezone
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField      # type: ignore
from phonenumber_field.modelfields import PhoneNumberField #type: ignore
from django.core.validators import FileExtensionValidator
from common.models import TimeStampedModel

User = get_user_model()

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
)

class Profile(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='O')
    country = CountryField(verbose_name=_("Country"), default="US")
    city = models.CharField(
        verbose_name=_("City"), max_length=180, default="Los Angeles"
    )
    address = models.CharField(max_length=255, null=True)
    zipcode = models.CharField(max_length=255, null=True)
    phone_number = PhoneNumberField(
        verbose_name=_("Phone Number"), 
        max_length=30, 
        default=""
    )
   

    def __str__(self) -> str:
        return f"{self.user.first_name}'s Profile"

    class Meta:
        db_table = 'profiles'
    
    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Workspace(TimeStampedModel):
    STATUS_CHOICES = (
        (0, 'Inactive'),
        (1, 'Active')
    )

    slug = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    is_globally_unsubscribed = models.BooleanField(default=False)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'workspaces'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()