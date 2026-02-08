import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dombackend.settings')
django.setup()

from django.contrib.auth import get_user_model
from accounts.models import StudentProfile

User = get_user_model()

def inspect_user():
    try:
        # Search by username or student_id
        user = User.objects.filter(username='test_payment_user').first()
        if not user:
            print("User 'test_payment_user' not found by username.")
            # Try finding by student ID 'TEST001'
            profile = StudentProfile.objects.filter(student_id='TEST001').first()
            if profile:
                user = profile.user
                print(f"Found user via Student ID TEST001: {user.username}")
            else:
                print("User not found by Student ID 'TEST001' either.")
                return

        print(f"User: {user.username}")
        print(f"Email: '{user.email}'")
        print(f"ID: {user.id}")
        
        if hasattr(user, 'studentprofile'):
            sp = user.studentprofile
            print(f"Student ID: {sp.student_id}")
            print(f"Gender: {sp.gender}")
            print(f"Department: {sp.department}")
            print(f"Year: {sp.year}")
            print(f"Phone: {getattr(sp, 'phone_number', 'N/A')}")
        else:
            print("No Student Profile found.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    inspect_user()
