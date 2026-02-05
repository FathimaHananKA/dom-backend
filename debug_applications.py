
import os
import django
import sys
import json

# Set up Django environment
sys.path.append(r"C:\Users\FATHIMA HANAN\Desktop\dombackend")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dombackend.settings')
django.setup()

from requests.models import DormApplication
from requests.serializers import DormApplicationSerializer

def debug_applications():
    apps = DormApplication.objects.all()
    print(f"Found {apps.count()} applications.")
    
    serializer = DormApplicationSerializer(apps, many=True)
    data = serializer.data
    
    print(json.dumps(data, indent=2, default=str))

if __name__ == "__main__":
    debug_applications()
