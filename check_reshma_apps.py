import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dombackend.settings')
django.setup()

from requests.models import DormApplication
from dormitories.models import Dormitory
from accounts.models import User

# Assume a warden user
warden_user = User.objects.get(username='Reshma')
print(f"Checking for warden: {warden_user.username}")
warden_profile = warden_user.wardenprofile

warden_dorms = Dormitory.objects.filter(assigned_warden=warden_profile)
print(f"Warden Dorms: {[d.name for d in warden_dorms]}")

queryset = DormApplication.objects.filter(
    preferred_dormitory__in=warden_dorms
)

print(f"Queryset count (before distinct): {queryset.count()}")
for app in queryset:
    print(f"  - App ID: {app.id}, Student: {app.student.student_id}, Dorm: {app.preferred_dormitory.name}")

queryset_distinct = queryset.distinct()
print(f"Queryset count (after distinct): {queryset_distinct.count()}")
for app in queryset_distinct:
    print(f"  - App ID: {app.id}, Student: {app.student.student_id}, Dorm: {app.preferred_dormitory.name}")
