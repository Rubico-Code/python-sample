import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    id = models.BigAutoField(primary_key=True, editable=False)
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at", "-updated_at"]
