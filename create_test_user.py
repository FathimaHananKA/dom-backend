import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dombackend.settings')
django.setup()

from django.contrib.auth import get_user_model
from accounts.models import StudentProfile, Role

User = get_user_model()

def create_test_user():
    username = 'test_payment_user'
    password = 'password123'
    student_id = 'TEST001'
    email = '' # "No Email" as per request/snippet
    
    if User.objects.filter(username=username).exists():
        print(f"User {username} already exists.")
        return

    print(f"Creating user {username}...")
    user = User.objects.create_user(username=username, email=email, password=password)
    
    # Assign Role
    student_role, _ = Role.objects.get_or_create(name='STUDENT')
    user.role = student_role
    user.save()
    
    # Create Profile
    StudentProfile.objects.create(
        user=user,
        student_id=student_id,
        department='UG',
        year='1',
        gender='FEMALE',
        phone_number='1234567890'
    )
    print(f"User {username} created successfully with Student ID {student_id}")

if __name__ == "__main__":
    create_test_user()
