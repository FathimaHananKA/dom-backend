
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dombackend.settings')
django.setup()

from dormitories.models import Dormitory
from dormitories.serializers import DormitorySerializer

def verify():
    print("Checking Dormitory model fields...")
    fields = [f.name for f in Dormitory._meta.get_fields()]
    if 'beds' in fields and 'number_of_beds' not in fields:
        print("SUCCESS: 'beds' field present, 'number_of_beds' removed.")
    else:
        print(f"FAILURE: Fields found: {fields}")

    print("\nChecking Serializer output...")
    # Create dummy instance
    try:
        d = Dormitory(name='TestDorm', gender='Male', total_rooms=10, beds=50)
        s = DormitorySerializer(d)
        data = s.data
        if 'beds' in data:
             print(f"SUCCESS: Serializer output contains 'beds': {data['beds']}")
        else:
             print(f"FAILURE: Serializer output missing 'beds'. Keys: {data.keys()}")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == '__main__':
    verify()
