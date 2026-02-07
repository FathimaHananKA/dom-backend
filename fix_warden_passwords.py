import os
import django
from django.db.models import Q

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dombackend.settings')
django.setup()

from accounts.models import User

def fix_passwords():
    print("--- Fixing Warden Passwords ---")
    wardens = User.objects.filter(role__name='WARDEN')
    
    affected_count = 0
    temp_password = "Warden@123"
    
    for u in wardens:
        # Check if password is not hashed
        if not u.password or not (u.password.startswith('pbkdf2_sha256$') or u.password.startswith('argon2$') or u.password.startswith('bcrypt$')):
            print(f"Fixing password for Warden: {u.username} (ID: {u.id})")
            u.set_password(temp_password)
            u.is_active = True # Ensure they are active too
            u.save()
            affected_count += 1
            
    print(f"\nSuccessfully reset {affected_count} warden passwords to: {temp_password}")
    print("Please inform the wardens to change their passwords after login.")

if __name__ == "__main__":
    fix_passwords()
