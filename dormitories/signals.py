from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Dormitory
from rooms.models import Room

# Signal disabled. Room creation is now handled in DormitorySerializer.create
# to support mixed room types.

# @receiver(post_save, sender=Dormitory)
# def create_rooms_for_dormitory(sender, instance, created, **kwargs):
#     pass
