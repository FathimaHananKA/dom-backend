import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dombackend.settings')
django.setup()

from accounts.models import User

def debug_login(username, password):
    print(f"Checking login for: {username}")
    user = User.objects.filter(username=username).first()
    if not user:
        print(f"FAILED: User '{username}' does not exist.")
        return
    
    print(f"User exists: {user.username} (ID: {user.id})")
    print(f"User is active: {user.is_active}")
    print(f"User is staff: {user.is_staff}")
    print(f"User is superuser: {user.is_superuser}")
    
    pw_match = user.check_password(password)
    print(f"Password '{password}' matches: {pw_match}")

if __name__ == "__main__":
    debug_login('admin', '987654321')
    debug_login('hanan@gmail.com', '987654321')
