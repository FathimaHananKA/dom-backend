import os
import django
from django.db.models import Q

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dombackend.settings')
django.setup()

from accounts.models import User

def force_reset(identifier, new_password):
    print(f"Force resetting password for identifier: {identifier}")
    candidates = User.objects.filter(Q(email=identifier) | Q(username=identifier))
    
    if not candidates.exists():
        print(f"FAILED: No users found matching '{identifier}'")
        return

    print(f"Found {candidates.count()} candidate(s).")
    for user in candidates:
        print(f"Updating User: {user.username} (ID: {user.id})")
        user.set_password(new_password)
        user.is_active = True
        user.save()
        print(f"  - Password set to: {new_password}")
        print(f"  - User activated.")

    print("\nSUCCESS: All matching accounts have been updated.")

if __name__ == "__main__":
    # You can change these values as needed
    target_identifier = "kafathimahanan@gmail.com" 
    target_password = "987654321"
    
    force_reset(target_identifier, target_password)
    
    # Also reset admin just in case
    force_reset("admin", "987654321")
