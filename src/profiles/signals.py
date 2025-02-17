import logging
from typing import Any, Type

from django.db.models.base import Model
from django.db.models.signals import post_save
from django.dispatch import receiver

from config.settings.base import AUTH_USER_MODEL
from profiles.models import Profile, Workspace

logger = logging.getLogger(__name__)


@receiver(post_save, sender=AUTH_USER_MODEL)
def create_user_profile_and_workspace(
    sender: Type[Model], instance: Model, created: bool, **kwargs: Any
) -> None:

    if created:
        Profile.objects.create(user=instance)
        Workspace.objects.create(
            slug=f"{instance.first_name}-workspace",
            title=f"{instance.first_name}'s Workspace",
            code=f"WS-{instance.unique_id}",
            status=1
        )
        logger.info(f"Profile created for {instance.first_name} {instance.last_name}")
    else:
        logger.info(
            f"Profile already exists for {instance.first_name} {instance.last_name}"
        )
