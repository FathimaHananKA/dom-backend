import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dombackend.settings')
django.setup()

from accounts.models import User

def reset_all_wardens():
    wardens = User.objects.filter(role__name='WARDEN')
    temp_password = "Warden@123"
    for u in wardens:
        u.set_password(temp_password)
        u.save()
    print(f"All {wardens.count()} wardens reset to: {temp_password}")

if __name__ == "__main__":
    reset_all_wardens()
