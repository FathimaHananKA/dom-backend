import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dombackend.settings')
django.setup()

from accounts.models import User
from django.db.models import Q

def force_reset(identifier, new_password):
    users = User.objects.filter(Q(username=identifier) | Q(email=identifier))
    if not users.exists():
        print(f"Oops! No user found matching: '{identifier}'")
        return

    print(f"Found {users.count()} matching account(s). Updating them all...")
    for user in users:
        user.set_password(new_password)
        user.is_active = True
        user.save()
        print(f"Successfully updated: {user.username} (ID: {user.id})")
    
    print("\nDONE! You can now log in with the new password.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python force_reset_v2.py <username_or_email> <new_password>")
    else:
        force_reset(sys.argv[1], sys.argv[2])
