from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from .models import Allocation
from .serializers import AllocationSerializer, AllocationListSerializer

from .serializers import MyAccommodationSerializer
from accounts.models import StudentProfile

class MyAccommodationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            student_profile = request.user.studentprofile
            allocation = Allocation.objects.get(student=student_profile)
            serializer = MyAccommodationSerializer(allocation)
            return Response(serializer.data)
        except StudentProfile.DoesNotExist:
            return Response(
                {"message": "User is not a student"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Allocation.DoesNotExist:
            return Response(
                {"message": "Accommodation not allocated yet"},
                status=status.HTTP_404_NOT_FOUND
            )

class AllocationViewSet(ModelViewSet):
    queryset = Allocation.objects.all()
    serializer_class = AllocationSerializer

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return AllocationListSerializer
        return AllocationSerializer

    def get_queryset(self):
        queryset = Allocation.objects.all()
        dormitory_id = self.request.query_params.get('dormitory', None)
        if dormitory_id is not None:
            # Filter by the room's dormitory
            queryset = queryset.filter(room__dormitory_id=dormitory_id)
        return queryset

    def send_allocation_email(self, allocation):
        # Send Email Notification
        try:
            from django.core.mail import send_mail
            from django.conf import settings
            
            student = allocation.student
            user = student.user
            room = allocation.bed.room
            bed_number = allocation.bed.bed_number
            dorm_name = room.dormitory.name
            
            subject = f'Room Allocation Update - {dorm_name}'
            message = f"""
Dear {user.username},

Your room allocation has been updated/confirmed.

Allocation Details:
------------------
Dormitory: {dorm_name}
Room Number: {room.room_number}
Bed Number: {bed_number}
Room Type: {room.room_type}

Please report to the warden for further instructions.

Best regards,
Dormitory Management Team
"""
            recipient_list = [user.email]
            if user.email:
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER, 
                    recipient_list,
                    fail_silently=False,
                )
                print(f"Email sent to {user.email}")
            else:
                print(f"No email found for user {user.username}")

        except Exception as e:
            print(f"Failed to send email: {str(e)}")

    def perform_create(self, serializer):
        allocation = serializer.save()
        self.send_allocation_email(allocation)

    def perform_update(self, serializer):
        allocation = serializer.save()
        self.send_allocation_email(allocation)


