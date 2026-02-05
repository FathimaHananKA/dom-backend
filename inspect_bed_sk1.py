import os
import django
import sys

# Add the project directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dombackend.settings')
django.setup()

from rooms.models import Room, Bed
from allocations.models import Allocation

def inspect_bed():
    print("Inspecting Bed SK1-1...")
    
    beds = Bed.objects.filter(bed_number__icontains='SK1-1')
    if not beds.exists():
        print("Bed 'SK1-1' not found. searching all beds in room SK1...")
        room = Room.objects.filter(room_number__icontains='SK1').first()
        if room:
            print(f"Found Room: {room}")
            beds = Bed.objects.filter(room=room)
        else:
            print("Room SK1 not found either.")
            return

    for bed in beds:
        print(f"Checking Bed: {bed.bed_number} (ID: {bed.id})")
        print(f"  Is Occupied: {bed.is_occupied}")
        
        allocation = Allocation.objects.filter(bed=bed).first()
        if allocation:
            print(f"  Allocation Found: ID {allocation.id}")
            print(f"  Student: {allocation.student}")
            try:
                print(f"  User: {allocation.student.user.username}")
            except:
                print("  User: <Missing>")
        else:
            print("  Allocation: NONE")
            
        if bed.is_occupied and not allocation:
            print("  [!] INCONSISTENCY FOUND: Bed is occupied but has no allocation.")
        elif not bed.is_occupied and allocation:
            print("  [!] INCONSISTENCY FOUND: Bed is NOT occupied but has allocation.")
        else:
            print("  Status seems consistent.")

if __name__ == '__main__':
    inspect_bed()
