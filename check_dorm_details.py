import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dombackend.settings')
django.setup()

from dormitories.models import Dormitory
print("--- Dormitory Details ---")
for d in Dormitory.objects.all():
    print(f"ID: {d.id} | Name: {d.name} | Gender: {d.gender} | Type: {d.type} | Category: {d.category}")
