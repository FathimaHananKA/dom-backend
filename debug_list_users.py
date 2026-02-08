import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dombackend.settings')
django.setup()

from django.contrib.auth import get_user_model
from accounts.models import StudentProfile

User = get_user_model()

def list_users():
    print("Listing all users:")
    for u in User.objects.all():
        student_id = "N/A"
        if hasattr(u, 'studentprofile'):
            student_id = u.studentprofile.student_id
        
        print(f"ID: {u.id} | Username: {u.username} | Email: '{u.email}' | StudentID: {student_id}")

if __name__ == "__main__":
    list_users()
