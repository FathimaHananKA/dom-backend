import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dombackend.settings')
django.setup()

from accounts.models import User

target_usernames = ['hgfddfvgbn', 'new333', 'hanan989']
new_pw = '12345678'

print("Checking and resetting specific accounts:")
for username in target_usernames:
    try:
        u = User.objects.get(username=username)
        u.set_password(new_pw)
        u.save()
        print(f"  - SUCCESS: {username} (Email: {u.email}) reset to '{new_pw}'. Matches reset: {u.check_password(new_pw)}")
    except User.DoesNotExist:
        print(f"  - NOT FOUND: {username}")

# Also check for any account using 'admin123' password? No, just reset to a known one.
print("\nInstructions for user:")
print(f"Use username: hanan989 OR hgfddfvgbn OR new333")
print(f"Use password: {new_pw}")
