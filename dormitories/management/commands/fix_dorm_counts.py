from django.core.management.base import BaseCommand
from dormitories.models import Dormitory
from rooms.models import Room


class Command(BaseCommand):
    help = 'Recalculate and fix dormitory total_rooms and total_beds counts'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Recalculating dormitory totals...'))
        
        dormitories = Dormitory.objects.all()
        fixed_count = 0
        
        for dorm in dormitories:
            # Get actual room count
            actual_rooms = Room.objects.filter(dormitory=dorm).count()
            
            # Calculate actual bed count
            actual_beds = sum(
                room.capacity for room in Room.objects.filter(dormitory=dorm)
            )
            
            # Check if correction is needed
            if dorm.total_rooms != actual_rooms or dorm.total_beds != actual_beds:
                old_rooms = dorm.total_rooms
                old_beds = dorm.total_beds
                
                # Update the dormitory
                dorm.total_rooms = actual_rooms
                dorm.total_beds = actual_beds
                dorm.save()
                
                fixed_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ Fixed {dorm.name}: '
                        f'{old_rooms}→{actual_rooms} rooms, '
                        f'{old_beds}→{actual_beds} beds'
                    )
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ {dorm.name}: Already correct ({actual_rooms} rooms, {actual_beds} beds)')
                )
        
        if fixed_count > 0:
            self.stdout.write(
                self.style.SUCCESS(f'\n✅ Fixed {fixed_count} dormitor{"y" if fixed_count == 1 else "ies"}')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('\n✅ All dormitories already have correct counts')
            )
