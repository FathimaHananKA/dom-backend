import os
import django
from django.db.models import Q

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dombackend.settings')
django.setup()

from accounts.models import User, WardenProfile, Role
from accounts.serializers import WardenProfileSerializer

def test_creation():
    print("Testing Warden Creation...")
    Role.objects.get_or_create(name='WARDEN')
    
    data = {
        'username': 'testwarden_new',
        'email': 'testwarden_new@gmail.com',
        'password': 'testpassword123',
        'employee_id': 'TEST_EMP_001',
        'phone_number': '1234567890',
        'gender': 'FEMALE'
    }
    
    serializer = WardenProfileSerializer(data=data)
    if serializer.is_valid():
        profile = serializer.save()
        user = profile.user
        print(f"Created Warden: {user.username}")
        print(f"Password in DB (first 15): {user.password[:15]}")
        print(f"Is Hashed properly: {user.password.startswith('pbkdf2_sha256$')}")
        print(f"Check password 'testpassword123': {user.check_password('testpassword123')}")
        
        # Cleanup
        # profile.delete()
        # user.delete()
    else:
        print(f"Serializer errors: {serializer.errors}")

if __name__ == "__main__":
    test_creation()
