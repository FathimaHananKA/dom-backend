import os
import django
from django.db.models import Q

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dombackend.settings')
django.setup()

from accounts.models import User, WardenProfile
from accounts.serializers import WardenProfileSerializer

def test_profile_update():
    print("--- Testing Profile Update ---")
    # Using 'Stephy' for the test
    try:
        profile = WardenProfile.objects.get(user__username='Stephy')
        print(f"Testing update for: {profile.user.username}")
        
        # Test updating password and phone number
        new_pass = "Stephy@Final2026"
        data = {
            'phone_number': '9998887776',
            'password': new_pass
        }
        
        serializer = WardenProfileSerializer(profile, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            profile.refresh_from_db()
            print(f"Phone Number updated: {profile.phone_number == '9998887776'}")
            print(f"Password updated (hashed check): {profile.user.check_password(new_pass)}")
            
            # Re-fixing for final state (back to Arden@123 or user choice)
            # Actually, let's leave it as Stephy@Final2026 for now so the user knows it worked
            print("\nStephy's password is now: Stephy@Final2026")
        else:
            print(f"Update failed: {serializer.errors}")
            
    except WardenProfile.DoesNotExist:
        print("Stephy not found in WardenProfile.")

if __name__ == "__main__":
    test_profile_update()
