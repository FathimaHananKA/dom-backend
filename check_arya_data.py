
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dombackend.settings')
django.setup()

from requests.models import Request, DormApplication
from requests.serializers import RequestSerializer, DormApplicationSerializer
from accounts.models import StudentProfile

def check_arya_data():
    try:
        student = StudentProfile.objects.get(student_id='S37')
        
        # Check Room Change Requests
        reqs = Request.objects.filter(student=student)
        print(f"Room Change Requests for S37: {reqs.count()}")
        for r in reqs:
            ser = RequestSerializer(r)
            print(f"  Req ID: {ser.data['id']}, Status: {ser.data['status']}, student_id: {ser.data.get('student_id')}")
            
        # Check Dorm Applications
        apps = DormApplication.objects.filter(student=student)
        print(f"Dorm Applications for S37: {apps.count()}")
        for a in apps:
            ser = DormApplicationSerializer(a)
            print(f"  App ID: {ser.data['id']}, Status: {ser.data['status']}, student_id: {ser.data.get('student_id')}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    check_arya_data()
