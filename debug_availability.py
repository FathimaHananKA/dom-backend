
import os
import django
from django.db.models import Count

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dombackend.settings')
django.setup()

from dormitories.models import Dormitory
from dormitories.serializers import DormitorySerializer

# Check all dorms
dorms = Dormitory.objects.all()
for dorm in dorms:
    serializer = DormitorySerializer(dorm)
    data = serializer.data
    print(f"Dorm: {dorm.name}")
    print(f"  Total Beds: {data.get('total_beds')}")
    print(f"  Occupied: {data.get('occupied_beds')}")
    print(f"  Available: {data.get('available_beds')}")
    print(f"  By Type: {data.get('availability_by_type')}")
    print("-" * 20)
