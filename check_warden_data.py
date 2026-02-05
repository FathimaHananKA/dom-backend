import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dombackend.settings')
django.setup()

from accounts.models import User, WardenProfile
from dormitories.models import Dormitory

# Inspect Wardens
wardens = WardenProfile.objects.all()
print(f"Total Wardens: {wardens.count()}")

for warden in wardens:
    print(f"Warden: {warden.user.username}")
    print(f"  Email: {warden.user.email}")
    print(f"  Phone: {warden.phone_number}")
    print(f"  Assigned Dorms: {[d.name for d in warden.dormitories.all()]}")

# Check specific dorm if known, or just list all
dorms = Dormitory.objects.all()
for dorm in dorms:
    print(f"Dorm: {dorm.name}")
    if dorm.assigned_warden:
         print(f"  Assigned Warden: {dorm.assigned_warden.user.username}")
    else:
         print(f"  Assigned Warden: None")
