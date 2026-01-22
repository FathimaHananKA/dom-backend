import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dombackend.settings")
django.setup()

from dormitories.serializers import DormitorySerializer
from dormitories.models import Dormitory
from rooms.models import Room

# 1. Setup Data
Dormitory.objects.filter(name="Update Test Dorm").delete()
dorm = Dormitory.objects.create(name="Update Test Dorm", gender="Male", total_rooms=2, total_beds=2)
# Create initial rooms
Room.objects.create(dormitory=dorm, room_number="U1", room_type="single", capacity=1)
Room.objects.create(dormitory=dorm, room_number="U2", room_type="single", capacity=1)

print(f"Initial: Rooms={dorm.total_rooms}, Beds={dorm.total_beds}, ActualRooms={Room.objects.filter(dormitory=dorm).count()}")

# 2. Update with new configs
serializer = DormitorySerializer(instance=dorm, data={
    "name": "Update Test Dorm (Edited)",
    "gender": "Male",
    "total_rooms": 100, # Legacy field, should be updated by serializer logic partially?
                        # Wait, backend update adds new_rooms_count to EXISTING total_rooms.
                        # But super().update() sets it to *this* value. 
                        # This is a conflict!
    "room_configurations": [
        {"prefix": "ADD", "count": 2, "type": "double"} # +2 rooms, +4 beds
    ]
}, partial=True)

if serializer.is_valid():
    dorm = serializer.save()
    print(f"Updated: Rooms={dorm.total_rooms}, Beds={dorm.total_beds}")
    
    # Check actual rooms
    rooms = Room.objects.filter(dormitory=dorm).order_by('room_number')
    for r in rooms:
        print(f"Room: {r.room_number}, Type: {r.room_type}")

    if dorm.total_rooms == 4 and dorm.total_beds == 6:
        print("SUCCESS: Totals updated correctly (2 initial + 2 new).")
    else:
        print("FAILURE: Totals mismatch.")
        # If I passed 100 in data, and super().update uses it, total_rooms might be 102?
        # My logic: instance = super().update(). instance.total_rooms += new.
        # So 100 + 2 = 102.
        # This confirms that passing "current total" in the payload is dangerous if we are doing incremental math.
        # But frontend sends (Base + New).
else:
    print(serializer.errors)
