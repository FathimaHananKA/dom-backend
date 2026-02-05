import os
import django
import sys

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dombackend.settings')
django.setup()

from accounts.models import User, WardenProfile
from dormitories.models import Dormitory

print("Checking Warden Data...")

wardens = WardenProfile.objects.all()
for w in wardens:
    print(f"Warden ID: {w.id}")
    print(f"  Username: {w.user.username}")
    print(f"  Email: {w.user.email}")
    print(f"  Phone: {w.phone_number}")
    print(f"  Employee ID: {w.employee_id}")
    dorms = w.dormitories.all()
    print(f"  Assigned Dorms: {[d.name for d in dorms]}")
    print("-" * 20)

if not wardens:
    print("No wardens found.")
