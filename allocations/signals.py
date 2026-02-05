from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Allocation

@receiver(post_delete, sender=Allocation)
def free_bed_on_allocation_delete(sender, instance, **kwargs):
    """
    Signal to automatically mark the associated bed as unoccupied
    when an Allocation is deleted.
    """
    if instance.bed:
        # Check if the bed still exists (it might be deleted too)
        try:
            bed = instance.bed
            bed.is_occupied = False
            bed.save()
            print(f"Signal: Marked {bed} as available after allocation deletion.")
        except Exception as e:
            print(f"Signal Error: Could not update bed status: {e}")
