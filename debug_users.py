import os
import django
import sys

# Setup Django environment
# Setup Django environment
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dombackend.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()
from django.db.models import Count

def check_users():
    print("--- User Account Debug ---")
    
    # Check for duplicates
    print("\n[Duplicate Emails]")
    duplicates = User.objects.values('email').annotate(count=Count('id')).filter(count__gt=1)
    if duplicates:
        for d in duplicates:
            print(f"Email '{d['email']}' has {d['count']} accounts.")
            users = User.objects.filter(email=d['email'])
            for u in users:
                print(f"  - ID: {u.id}, Username: {u.username}, Active: {u.is_active}, Role: {getattr(u, 'role', 'N/A')}")
    else:
        print("No duplicate emails found.")

    print("\n[User List]")
    users = User.objects.all().order_by('-date_joined')[:20]
    for u in users:
        print(f"ID: {u.id} | Username: {u.username} | Email: {u.email} | Active: {u.is_active} | Role: {u.role.name if u.role else 'None'}")

if __name__ == '__main__':
    check_users()
