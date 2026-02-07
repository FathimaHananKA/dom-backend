import os
import django
from django.db.models import Q

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dombackend.settings')
django.setup()

from accounts.models import User

def check_stephy():
    identifier = "Stephy"
    users = User.objects.filter(Q(username=identifier) | Q(email=identifier))
    print(f"Checking for '{identifier}': Found {users.count()} users.")
    for u in users:
        print(f"ID: {u.id}, Username: {u.username}, Email: {u.email}")
        print(f"Password (first 15 chars): {u.password[:15]}")
        print(f"Is Hashed: {u.password.startswith('pbkdf2_sha256$')}")
        print(f"Check with '12345678': {u.check_password('12345678')}")

if __name__ == "__main__":
    check_stephy()
