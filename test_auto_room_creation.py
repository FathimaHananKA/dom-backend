import os
import django
import sys

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dombackend.settings')
django.setup()

from dormitories.models import Dormitory
from rooms.models import Room

def test_room_creation():
    dorm_name = "Test Auto Dorm"
    prefix = "T"
    count = 5
    
    # Clean up previous runs
    Dormitory.objects.filter(name=dorm_name).delete()
    
    print(f"Creating Dormitory '{dorm_name}' with {count} rooms and prefix '{prefix}'...")
    dorm = Dormitory.objects.create(
        name=dorm_name,
        gender="Male",
        total_rooms=count,
        total_beds=count * 2,
        room_prefix=prefix
    )
    
    # Check rooms
    rooms = Room.objects.filter(dormitory=dorm)
    print(f"Found {rooms.count()} rooms for dormitory '{dorm.name}'.")
    
    if rooms.count() != count:
        print(f"FAILED: Expected {count} rooms, found {rooms.count()}")
        return

    # Check room names
    param_names = [r.room_number for r in rooms]
    print(f"Room numbers: {sorted(param_names)}")
    
    expected_names = [f"{prefix}{i}" for i in range(1, count + 1)]
    
    if sorted(param_names) == sorted(expected_names):
        print("SUCCESS: Room names match expected sequence.")
    else:
        print(f"FAILED: Room names do not match. Expected {expected_names}")

if __name__ == "__main__":
    test_room_creation()
