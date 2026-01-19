import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dombackend.settings')
django.setup()
from rooms.models import Room
print(f"Room count: {Room.objects.count()}")
for r in Room.objects.all():
    print(f"Room: {r.room_number}, Dorm: {r.dormitory.name}, Capacity: {r.capacity}, Type: {r.room_type}")
