import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dombackend.settings')
django.setup()

from requests.models import DormApplication
from dormitories.models import Dormitory

sid = 'S37'
print(f"--- Arya Application Details ---")
apps = DormApplication.objects.filter(student__student_id=sid)
for app in apps:
    dorm = app.preferred_dormitory
    warden_profile = dorm.assigned_warden
    warden_user = warden_profile.user if warden_profile else None
    print(f"App ID: {app.id}, Status: {app.status}, Preferred Dorm: {dorm.name}")
    print(f"Warden for this dorm: {warden_user.username if warden_user else 'None'}")
    
    if warden_profile:
        all_dorms_for_warden = Dormitory.objects.filter(assigned_warden=warden_profile)
        print(f"All dorms for this warden: {[d.name for d in all_dorms_for_warden]}")
        
        # Simulating the queryset duplication
        qs = DormApplication.objects.filter(preferred_dormitory__in=all_dorms_for_warden)
        print(f"Queryset for this warden (all): {qs.count()}")
        print(f"Queryset for this warden (distinct): {qs.distinct().count()}")
        
        for item in qs:
            if item.student.student_id == sid:
                print(f"  - Match: App ID {item.id}, Student {item.student.student_id}")

print(f"\nSearching for ANY other student named Arya...")
from accounts.models import User
for u in User.objects.filter(username__icontains='Arya'):
    print(f"Found User: {u.username}, Student ID: {u.studentprofile.student_id if hasattr(u, 'studentprofile') else 'N/A'}")
