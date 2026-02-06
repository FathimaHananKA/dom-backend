import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dombackend.settings')
django.setup()

from accounts.models import User

def check_hgf():
    identifier = "hgfddfvgbn"
    users = User.objects.filter(models.Q(username=identifier) | models.Q(email=identifier))
    print(f"Checking for identifier: '{identifier}'")
    print(f"Found {users.count()} users.")
    for u in users:
        print(f"ID: {u.id} | Username: {u.username} | Email: {u.email} | Active: {u.is_active}")

if __name__ == "__main__":
    from django.db import models
    check_hgf()
