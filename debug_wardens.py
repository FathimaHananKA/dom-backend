import os
import django
from django.db.models import Q

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dombackend.settings')
django.setup()

from accounts.models import User, WardenProfile

def check_wardens():
    print("Checking Warden Accounts...")
    wardens = User.objects.filter(role__name='WARDEN')
    print(f"Total Wardens found: {wardens.count()}")
    
    for u in wardens:
        print(f"\nUsername: {u.username}")
        print(f"Email: {u.email}")
        print(f"ID: {u.id}")
        print(f"Is Active: {u.is_active}")
        print(f"Has Password: {u.has_usable_password()}")
        # Check if password starts with a standard Django hash prefix
        is_hashed = u.password.startswith('pbkdf2_sha256$') or u.password.startswith('argon2$') or u.password.startswith('bcrypt$')
        print(f"Password appears hashed: {is_hashed}")
        if not is_hashed:
            print(f"WARNING: Password for {u.username} seems to be plain text or unknown format: {u.password[:10]}...")
            
        # Check for duplicates
        duplicates = User.objects.filter(Q(username=u.username) | Q(email=u.email)).exclude(id=u.id)
        if duplicates.exists():
            print(f"WARNING: Found {duplicates.count()} potential duplicate(s) for {u.username}")
            for d in duplicates:
                print(f"  - Duplicate ID: {d.id}, Username: {d.username}, Email: {d.email}, Role: {d.role.name if d.role else 'None'}")

if __name__ == "__main__":
    check_wardens()
