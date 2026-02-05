from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class Role(models.Model):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('WARDEN', 'Warden'),
        ('STUDENT', 'Student'),
    )

    name = models.CharField(max_length=20, choices=ROLE_CHOICES, unique=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.username

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(
        max_length=10,
        choices=(('UG','Ug'),('PG','Pg'))
    )
    year = models.IntegerField()
    gender = models.CharField(
        max_length=10,
        choices=(('MALE', 'Male'), ('FEMALE', 'Female'))
    )
    can_change_room = models.BooleanField(default=False)

    def __str__(self):
        return self.student_id

class WardenProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=15)
    gender = models.CharField(
        max_length=10,
        choices=(('MALE', 'Male'), ('FEMALE', 'Female')),
        default='MALE'
    )

    def __str__(self):
        return self.employee_id

