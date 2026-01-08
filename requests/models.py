from django.db import models
from accounts.models import StudentProfile
from rooms.models import Room

class Request(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )

    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='requests'
    )
    current_room = models.ForeignKey(
        Room,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='current_requests'
    )
    preferred_room = models.ForeignKey(
        Room,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='preferred_requests'
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='Pending'
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username} → {self.status}"
