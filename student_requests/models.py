from django.db import models
from accounts.models import StudentProfile
from rooms.models import Room
from dormitories.models import Dormitory 

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
    preferred_dormitory = models.ForeignKey(
        Dormitory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='room_change_requests'
    )
    room_type_preference = models.CharField(
        max_length=20,
        choices=(
            ('single', 'Single'),
            ('double', 'Double'),
            ('triple', 'Triple'),
        ),
        null=True,
        blank=True
    )
    preferred_room = models.ForeignKey(
        Room,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='preferred_requests'
    )
    reason = models.TextField(null=True, blank=True)
    current_bed_number = models.CharField(max_length=20, null=True, blank=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='Pending'
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    requested_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'requests_request'

    def __str__(self):
        return f"{self.student.user.username} → {self.status}"



class DormApplication(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    )

    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='dorm_applications'
    )
    preferred_dormitory = models.ForeignKey(
        Dormitory,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    room_preference = models.CharField(
        max_length=20,
        choices=(
            ('single', 'Single'),
            ('double', 'Double'),
            ('triple', 'Triple'),
        ),
        null=True,
        blank=True
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'requests_dormapplication'

    def __str__(self):
        return f"{self.student.user.username} → {self.preferred_dormitory.name} ({self.status})"


class NewStudentRequest(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )

    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='new_student_requests'
    )
    preferred_dormitory = models.ForeignKey(
        Dormitory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='new_student_requests'
    )
    room_type_preference = models.CharField(
        max_length=20,
        choices=(
            ('single', 'Single'),
            ('double', 'Double'),
            ('triple', 'Triple'),
        ),
        null=True,
        blank=True
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='Pending'
    )
    reason = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'requests_newstudentrequest'

    def __str__(self):
        return f"New Request: {self.student.user.username} - {self.status}"
