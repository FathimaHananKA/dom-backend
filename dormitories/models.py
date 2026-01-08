from django.db import models
from accounts.models import WardenProfile

class Dormitory(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

    name = models.CharField(max_length=100, unique=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    total_rooms = models.PositiveIntegerField()

    assigned_warden = models.ForeignKey(
        WardenProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='dormitories'
    )

    def __str__(self):
        return self.name
