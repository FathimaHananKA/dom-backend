import os
import django
import sys

# Set up Django environment
sys.path.append(r'c:\Users\FATHIMA HANAN\Desktop\dombackend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dombackend.settings')
django.setup()

from student_requests.models import Request, DormApplication
from accounts.models import StudentProfile
from dormitories.models import Dormitory
from student_requests.serializers import RequestSerializer, DormApplicationSerializer
from rest_framework.exceptions import ValidationError

def test_update_validation():
    # 1. Test Request Update
    print("Testing Request update validation...")
    student = StudentProfile.objects.first()
    dorm = Dormitory.objects.first()
    
    # Create a pending request
    req, created = Request.objects.get_or_create(
        student=student, 
        status='Pending', 
        defaults={'preferred_dormitory': dorm, 'reason': 'Initial'}
    )
    
    # Attempt to update it (simulate Warden approval)
    serializer = RequestSerializer(req, data={'status': 'Approved'}, partial=True)
    # Mock request context
    class MockRequest:
        def __init__(self, user):
            self.user = user
    serializer.context['request'] = MockRequest(student.user)
    
    try:
        serializer.is_valid(raise_exception=True)
        print("PASSED: Request update allowed (self excluded from validation).")
        serializer.save()
        print(f"Request status updated to: {req.status}")
    except ValidationError as e:
        print(f"FAILED: Request update blocked by validation: {e}")

    # 2. Test DormApplication Update
    print("\nTesting DormApplication update validation...")
    app, created = DormApplication.objects.get_or_create(
        student=student, 
        status='PENDING', 
        defaults={'preferred_dormitory': dorm}
    )
    
    app_serializer = DormApplicationSerializer(app, data={'status': 'APPROVED'}, partial=True)
    app_serializer.context['request'] = MockRequest(student.user)
    
    try:
        app_serializer.is_valid(raise_exception=True)
        print("PASSED: DormApplication update allowed.")
        app_serializer.save()
        print(f"Application status updated to: {app.status}")
    except ValidationError as e:
        print(f"FAILED: DormApplication update blocked: {e}")

    # Reset for testing (optional)
    # req.status = 'Pending'
    # req.save()

if __name__ == "__main__":
    test_update_validation()
