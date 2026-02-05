import os
import django
import sys

# Add the project root to the python path
backend_path = r"c:\Users\FATHIMA HANAN\Desktop\dombackend"
if backend_path not in sys.path:
    sys.path.append(backend_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dormmanager.settings')
django.setup()

from dormitories.models import Dormitory

print(f"{'ID':<4} | {'Name':<20} | {'Gender':<10} | {'Type':<5} | {'Category':<8}")
print("-" * 70)

for dorm in Dormitory.objects.all():
    print(f"{dorm.id:<4} | {dorm.name:<20} | {dorm.gender:<10} | {dorm.type:<5} | {dorm.category:<8}")
