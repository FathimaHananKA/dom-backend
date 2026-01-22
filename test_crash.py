import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dombackend.settings")
django.setup()

from dormitories.serializers import DormitorySerializer
from dormitories.models import Dormitory
from rooms.models import Room, Bed

# 1. Setup
Dormitory.objects.filter(name="Crash Test Dorm").delete()

data = {
    "name": "Crash Test Dorm",
    "gender": "Male",
    "room_configurations": [
        {"startName": "SuperLongPrefixThatExceedsLimit", "count": 1, "type": "single"}, # Should crash?
        {"startName": "Normal", "count": 1, "type": "single"}
    ]
}

print("Attempting to create with long prefix...")
try:
    serializer = DormitorySerializer(data=data)
    if serializer.is_valid():
        dorm = serializer.save()
        print("Success (Unexpected if validation failed?)")
    else:
        print("Validation Error:", serializer.errors)
except Exception as e:
    print(f"Caught Exception: {e}")

# CHECK BEDS
if Dormitory.objects.filter(name="Crash Test Dorm").exists():
    dorm = Dormitory.objects.get(name="Crash Test Dorm")
    rooms = Room.objects.filter(dormitory=dorm)
    for r in rooms:
        bed_count = Bed.objects.filter(room=r).count()
        print(f"Room {r.room_number}: Beds={bed_count} (Expected {r.capacity})")
        
