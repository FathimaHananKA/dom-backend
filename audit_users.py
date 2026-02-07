import os
import django
from django.db.models import Q, Count

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dombackend.settings')
django.setup()

from accounts.models import User

def audit_users():
    print("--- User Audit ---")
    all_users = User.objects.all()
    print(f"Total Users: {all_users.count()}")
    
    invalid_pws = []
    for u in all_users:
        if not u.password or not (u.password.startswith('pbkdf2_sha256$') or u.password.startswith('argon2$') or u.password.startswith('bcrypt$')):
            invalid_pws.append(u)
            
    print(f"\nUsers with invalid/plain/empty passwords: {len(invalid_pws)}")
    for u in invalid_pws:
        role = u.role.name if u.role else "None"
        print(f"ID: {u.id} | Username: {u.username} | Email: {u.email} | Role: {role} | Joined: {u.date_joined} | PW: {repr(u.password[:10])}...")

    print("\n--- Duplicate Checking ---")
    emails = User.objects.values('email').annotate(count=Count('id')).filter(count__gt=1)
    print(f"Emails with multiple accounts: {emails.count()}")
    for e in emails:
        print(f"\nEmail: {e['email']}")
        users = User.objects.filter(email=e['email'])
        for u in users:
            print(f"  - ID: {u.id}, Username: {u.username}, Role: {u.role.name if u.role else 'None'}, Active: {u.is_active}")

    usernames = User.objects.values('username').annotate(count=Count('id')).filter(count__gt=1)
    print(f"\nUsernames with multiple accounts: {usernames.count()}")
    for u_name in usernames:
        print(f"\nUsername: {u_name['username']}")
        users = User.objects.filter(username=u_name['username'])
        for u in users:
            print(f"  - ID: {u.id}, Email: {u.email}, Role: {u.role.name if u.role else 'None'}, Active: {u.is_active}")

if __name__ == "__main__":
    audit_users()
