
import os
import django
import sys

# Add the project directory to sys.path
sys.path.append(os.getcwd())

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dombackend.settings')
django.setup()

from accounts.models import User
from django.db.models import Count

def check_duplicates():
    print("Checking for duplicate emails...")
    duplicate_emails = User.objects.values('email').annotate(email_count=Count('email')).filter(email_count__gt=1)
    
    if not duplicate_emails:
        print("No duplicate emails found.")
    else:
        for entry in duplicate_emails:
            email = entry['email']
            count = entry['email_count']
            print(f"\nEmail: {email} (Count: {count})")
            users = User.objects.filter(email=email)
            for user in users:
                print(f"  - Username: {user.username}, ID: {user.id}, Is Active: {user.is_active}")

if __name__ == "__main__":
    check_duplicates()
