from django.db import models
from accounts.models import StudentProfile
from rooms.models import Bed


class Allocation(models.Model):
    student = models.OneToOneField(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='allocation'
    )
    bed = models.OneToOneField(
        Bed,
        on_delete=models.CASCADE,
        related_name='allocation'
    )
    allocated_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student} → {self.bed}"
