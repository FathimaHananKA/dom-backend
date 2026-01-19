from django.db import models
from dormitories.models import Dormitory

class Room(models.Model):
    room_number = models.CharField(max_length=10)
    dormitory = models.ForeignKey(
        Dormitory,
        on_delete=models.CASCADE,
        related_name='rooms'
    )
    floor = models.PositiveIntegerField(default=1)
    room_type = models.CharField(
        max_length=10,
        choices=(
            ('single', 'Single'),
            ('double', 'Double'),
            ('triple', 'Triple'),
            ('quad', 'Quad')
        ),
        default='double'
    )
    capacity = models.IntegerField(default=2)

    def __str__(self):
        return f"{self.room_number} - {self.dormitory.name}"


class Bed(models.Model):
    bed_number = models.CharField(max_length=10)
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='beds'
    )
    is_occupied = models.BooleanField(default=False)

    def __str__(self):
        status = "Occupied" if self.is_occupied else "Available"
        return f"Bed {self.bed_number} - {self.room.room_number} ({status})"
