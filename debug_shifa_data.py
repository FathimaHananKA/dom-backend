import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dombackend.settings')
django.setup()

from accounts.models import User

def check_all_users():
    print("Checking ALL Users...")
    users = User.objects.all()
    print(f"Total Users: {users.count()}")
    
    for u in users:
        print(f"\nUser: {u.username} (ID: {u.id})")
        try:
            profile = getattr(u, 'studentprofile', None)
            if not profile:
                print("  - No Student Profile")
                continue
                
            allocation = getattr(profile, 'allocation', None)
            if allocation:
                print(f"  - Allocation ID: {allocation.id}")
                print(f"  - Allocation.is_paid: {allocation.is_paid}")
            else:
                print("  - No Allocation found")
                
            payments = profile.payments.all()
            if payments.exists():
                print("  - Payments:")
                for p in payments:
                    print(f"    * ID: {p.id}, Status: {p.status}, AllocID: {p.allocation_id}")
            else:
                print("  - No Payments")
                
        except Exception as e:
            print(f"  - Error: {e}")

if __name__ == "__main__":
    check_all_users()
