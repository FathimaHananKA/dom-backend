from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Allocation


@receiver(post_delete, sender=Allocation)
def mark_bed_available_on_delete(sender, instance, **kwargs):
    """
    When an allocation is deleted, mark the bed as available
    """
    if instance.bed:
        instance.bed.is_occupied = False
        instance.bed.save()
