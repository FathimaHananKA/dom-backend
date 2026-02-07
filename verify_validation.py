import os
import django
import sys

# Set up Django environment
sys.path.append(r'c:\Users\FATHIMA HANAN\Desktop\dombackend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dombackend.settings')
django.setup()

from student_requests.models import Request, DormApplication, NewStudentRequest
from accounts.models import StudentProfile
from dormitories.models import Dormitory
from student_requests.serializers import RequestSerializer, DormApplicationSerializer, NewStudentRequestSerializer
from rest_framework.exceptions import ValidationError

def test_validation():
    # Get a student profile
    student = StudentProfile.objects.first()
    if not student:
        print("No student profile found for testing.")
        return

    print(f"Testing validation for student: {student.user.username}")

    # 1. Test Request validation
    print("\n1. Testing Request validation...")
    # Ensure a pending request exists
    Request.objects.get_or_create(student=student, status='Pending', defaults={'reason': 'Test'})
    
    dorm = Dormitory.objects.first()
    serializer = RequestSerializer(data={'preferred_dormitory': dorm.id, 'room_type_preference': 'single', 'reason': 'Another test'})
    # Mock request context
    class MockRequest:
        def __init__(self, user):
            self.user = user
    
    serializer.context['request'] = MockRequest(student.user)
    
    try:
        serializer.is_valid(raise_exception=True)
        print("FAILED: Request validation allowed duplicate pending request.")
    except ValidationError as e:
        print(f"PASSED: Received expected validation error: {e}")

    # 2. Test DormApplication validation
    print("\n2. Testing DormApplication validation...")
    dorm = Dormitory.objects.first()
    DormApplication.objects.get_or_create(student=student, preferred_dormitory=dorm, status='PENDING')
    
    app_serializer = DormApplicationSerializer(data={'preferred_dormitory': dorm.id, 'room_preference': 'single'})
    app_serializer.context['request'] = MockRequest(student.user)
    
    try:
        app_serializer.is_valid(raise_exception=True)
        print("FAILED: DormApplication validation allowed duplicate pending application.")
    except ValidationError as e:
        print(f"PASSED: Received expected validation error: {e}")

    # Clean up (optional, but good for repeatability)
    # Request.objects.filter(student=student, status='Pending', reason='Test').delete()
    # DormApplication.objects.filter(student=student, status='PENDING').delete()

if __name__ == "__main__":
    test_validation()
