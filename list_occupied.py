import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dombackend.settings')
django.setup()

from rooms.models import Bed

def list_occupied_beds():
    occupied = Bed.objects.filter(is_occupied=True)
    print(f"Total Occupied Beds: {occupied.count()}")
    for bed in occupied:
        print(f"- {bed.bed_number} (Room {bed.room.room_number})")
        # Check allocation
        if hasattr(bed, 'allocation'):
             print(f"  -> Allocation exists: {bed.allocation.student.student_id}")
        else:
             print(f"  -> NO ALLOCATION (Inconsistent!)")

if __name__ == '__main__':
    list_occupied_beds()
