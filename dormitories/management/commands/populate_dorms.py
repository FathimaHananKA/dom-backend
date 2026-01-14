from django.core.management.base import BaseCommand
from dormitories.models import Dormitory
from rooms.models import Room, Bed


class Command(BaseCommand):
    help = 'Populate the database with sample dormitories, rooms, and beds'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample dormitories...')

        # Create dormitories
        dorms_data = [
            {'name': 'Sunrise Hall', 'gender': 'Male', 'total_rooms': 20},
            {'name': 'Moonlight Residence', 'gender': 'Female', 'total_rooms': 20},
            {'name': 'Phoenix Tower', 'gender': 'Male', 'total_rooms': 25},
        ]

        for dorm_data in dorms_data:
            dorm, created = Dormitory.objects.get_or_create(
                name=dorm_data['name'],
                defaults={
                    'gender': dorm_data['gender'],
                    'total_rooms': dorm_data['total_rooms']
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created dormitory: {dorm.name}'))
                
                # Create rooms for this dormitory
                for room_num in range(1, dorm_data['total_rooms'] + 1):
                    room = Room.objects.create(
                        room_number=f'{room_num:03d}',
                        dormitory=dorm
                    )
                    
                    # Create 2 beds per room
                    for bed_num in range(1, 3):
                        Bed.objects.create(
                            bed_number=f'B{bed_num}',
                            room=room,
                            is_occupied=False
                        )
                
                self.stdout.write(self.style.SUCCESS(
                    f'  Added {dorm_data["total_rooms"]} rooms with 2 beds each'
                ))
            else:
                self.stdout.write(self.style.WARNING(f'Dormitory already exists: {dorm.name}'))

        self.stdout.write(self.style.SUCCESS('\nDone! Database populated successfully.'))
