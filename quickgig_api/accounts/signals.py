from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import BaseUser, TaskerProfile


@receiver(post_save, sender=BaseUser)
def create_tasker_profile(sender, instance, created, **kwargs):
    # If the user is a tasker but doesn't have a profile, create one
    if instance.is_tasker and not hasattr(instance, 'tasker_profile'):
        TaskerProfile.objects.get_or_create(user=instance)
