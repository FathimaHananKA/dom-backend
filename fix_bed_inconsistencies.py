import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dombackend.settings')
django.setup()

from rooms.models import Bed
from allocations.models import Allocation

def fix_orphaned_beds():
    print("Checking for orphaned occupied beds...")
    occupied_beds = Bed.objects.filter(is_occupied=True)
    fixed_count = 0
    
    for bed in occupied_beds:
        # Check if this bed has an allocation
        # Since Allocation has OneToOne to Bed with related_name='allocation',
        # we can check via the reverse accessor or query Allocation directly.
        
        has_allocation = Allocation.objects.filter(bed=bed).exists()
        
        if not has_allocation:
            print(f"Bed {bed.bed_number} in Room {bed.room.room_number} ({bed.room.dormitory.name}) is marked occupied but has no allocation. Fixing...")
            bed.is_occupied = False
            bed.save()
            fixed_count += 1
            
    print(f"Finished. Fixed {fixed_count} orphaned beds.")

if __name__ == '__main__':
    fix_orphaned_beds()
