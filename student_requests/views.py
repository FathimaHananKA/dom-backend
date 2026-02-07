from rest_framework.viewsets import ModelViewSet
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from .models import Request, DormApplication, NewStudentRequest
from .serializers import RequestSerializer, DormApplicationSerializer, NewStudentRequestSerializer

# Existing Room Change Requests
class RequestViewSet(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RequestSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Request.objects.all()
            
        # Warden can see requests involving their dormitory
        if hasattr(user, 'wardenprofile'):
            from dormitories.models import Dormitory
            warden_dorms = Dormitory.objects.filter(assigned_warden=user.wardenprofile)
            if warden_dorms.exists():
                return Request.objects.filter(
                    Q(student__user=user) | 
                    Q(current_room__dormitory__in=warden_dorms) | 
                    Q(preferred_dormitory__in=warden_dorms)
                ).distinct()

        return Request.objects.filter(student__user=user)

    def perform_update(self, serializer):
        status = serializer.validated_data.get('status')
        if status in ['Approved', 'Rejected']:
            from django.utils import timezone
            serializer.save(reviewed_at=timezone.now())
        else:
            serializer.save()

    def perform_create(self, serializer):
        # Automatically assign the logged-in student's profile and current room
        student_profile = self.request.user.studentprofile
        current_room = None
        current_bed_number = None # Initialize to None instead of "N/A"
        
        # Try to find current room and bed from allocation
        try:
            if hasattr(student_profile, 'allocation') and student_profile.allocation:
                current_room = student_profile.allocation.bed.room
                current_bed_number = student_profile.allocation.bed.bed_number
        except Exception:
            pass

        # Check for existing pending requests
        has_allocation = hasattr(student_profile, 'allocation') and student_profile.allocation is not None
        
        pending_requests = Request.objects.filter(student=student_profile, status='Pending').exists()
        # If student has allocation, we ignore the 'PENDING' status of initial apps
        pending_apps = not has_allocation and DormApplication.objects.filter(student=student_profile, status='PENDING').exists()
        pending_new = NewStudentRequest.objects.filter(student=student_profile, status='Pending').exists()

        if pending_requests or pending_apps or pending_new:
            from rest_framework.exceptions import ValidationError
            raise ValidationError({'detail': 'You already have a pending request. Please wait for it to be processed.'})

        request_obj = serializer.save(
            student=student_profile, 
            current_room=current_room,
            current_bed_number=current_bed_number
        )

        # Send Email Notification
        try:
            from django.core.mail import send_mail
            from django.conf import settings
            
            user = self.request.user
            preferred_dorm = request_obj.preferred_dormitory.name if request_obj.preferred_dormitory else "Any"
            
            subject = 'Room Change Request Submitted'
            message = f"""
Dear {user.username},

Your request for a room change has been submitted successfully.

Request Details:
----------------
Preferred Dormitory: {preferred_dorm}
Preferred Room Type: {request_obj.room_type_preference}
Reason: {request_obj.reason}

The warden will review your request and you will be notified of the outcome.

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
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def warden_requests(self, request):
        """
        Fetch room change requests for students in the warden's dormitory.
        Supports ?status=Pending (default), ?status=processed, or ?status=all
        """
        try:
            # Check if user is a warden
            if not hasattr(request.user, 'wardenprofile'):
                return Response({'detail': 'User is not a warden'}, status=403)
            
            # Get warden's assigned dormitories
            from dormitories.models import Dormitory
            warden_dorms = Dormitory.objects.filter(assigned_warden=request.user.wardenprofile)
            if not warden_dorms.exists():
                 return Response({'detail': 'No dormitory assigned'}, status=404)
            
            # Base query
            queryset = Request.objects.filter(
                Q(current_room__dormitory__in=warden_dorms) | Q(preferred_dormitory__in=warden_dorms)
            ).distinct()

            # Filter by status
            status = request.query_params.get('status', 'all')
            if status.lower() == 'processed':
                queryset = queryset.exclude(status='Pending')
            elif status.lower() != 'all':
                queryset = queryset.filter(status=status)
            
            queryset = queryset.select_related(
                'student', 'student__user', 'current_room', 
                'preferred_dormitory', 'preferred_room'
            ).order_by('-requested_at')
            
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            return Response({'detail': str(e)}, status=500)


# Dorm Application Views

class DormApplicationCreateView(generics.CreateAPIView):
    """
    Allow a student to apply for a dormitory.
    """
    serializer_class = DormApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically assign the logged-in student
        student_profile = self.request.user.studentprofile

        # Check for existing pending requests
        pending_requests = Request.objects.filter(student=student_profile, status='Pending').exists()
        pending_apps = DormApplication.objects.filter(student=student_profile, status='PENDING').exists()
        pending_new = NewStudentRequest.objects.filter(student=student_profile, status='Pending').exists()

        if pending_requests or pending_apps or pending_new:
            from rest_framework.exceptions import ValidationError
            raise ValidationError({'detail': 'You already have a pending request. Please wait for it to be processed.'})

        application = serializer.save(student=student_profile)
        
        # Send Application Received Email
        try:
            from django.core.mail import send_mail
            from django.conf import settings
            
            user = self.request.user
            dorm_name = application.preferred_dormitory.name
            
            subject = f'Dormitory Application Received - {dorm_name}'
            message = f"""
Dear {user.username},

We have received your application for {dorm_name}.

Application Details:
--------------------
Dormitory: {dorm_name}
Room Preference: {application.room_preference}
Status: Pending

The warden will review your application shortly.

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
        except Exception as e:
            print(f"Failed to send application email: {str(e)}")


class DormApplicationDetailView(generics.RetrieveAPIView):
    """
    Retrieve the current logged-in student's dorm application.
    """
    serializer_class = DormApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Return the dorm application for the logged-in student
        student_profile = self.request.user.studentprofile
        # Return the latest dorm application for the logged-in student
        return DormApplication.objects.filter(student=student_profile).order_by('-created_at').first()
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is None:
            return Response({'application': None}, status=200)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class DormApplicationListView(generics.ListAPIView):
    """
    List all dorm applications (Admin only).
    """
    queryset = DormApplication.objects.all()
    serializer_class = DormApplicationSerializer
    # Allow Wardens to update applications
    permission_classes = [permissions.IsAuthenticated]


class WardenDormApplicationsView(generics.ListAPIView):
    """
    List pending dorm applications for the warden's assigned dormitory.
    """
    serializer_class = DormApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Check if user is a warden
        if not hasattr(self.request.user, 'wardenprofile'):
            return DormApplication.objects.none()
        
        # Get warden's assigned dormitories
        from dormitories.models import Dormitory
        warden_dorms = Dormitory.objects.filter(assigned_warden=self.request.user.wardenprofile)
        if not warden_dorms.exists():
            return DormApplication.objects.none()
        
        # Base query
        queryset = DormApplication.objects.filter(
            preferred_dormitory__in=warden_dorms
        ).distinct()
        
        # Filter by status
        status = self.request.query_params.get('status', 'all')
        if status.lower() == 'processed':
            queryset = queryset.exclude(status='PENDING')
        elif status.lower() != 'all':
            queryset = queryset.filter(status=status)
            
        return queryset.select_related('student', 'student__user', 'preferred_dormitory').order_by('-created_at')


class AdminDormApplicationDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a dorm application (Admin and Warden).
    """
    serializer_class = DormApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Admin can see all
        if user.is_staff or user.is_superuser:
            return DormApplication.objects.all()
        
        # Warden can see/edit applications for their dormitory
        if hasattr(user, 'wardenprofile'):
            from dormitories.models import Dormitory
            warden_dorms = Dormitory.objects.filter(assigned_warden=user.wardenprofile)
            if warden_dorms.exists():
                return DormApplication.objects.filter(preferred_dormitory__in=warden_dorms).distinct()
        
        return DormApplication.objects.none()

    def get_serializer_class(self):
        # Use simple serializer for reading, but one with writable status for updating?
        # Actually easier to use the AdminSerializer properly
        from .serializers import AdminDormApplicationSerializer
        return AdminDormApplicationSerializer


class NewStudentRequestViewSet(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NewStudentRequestSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return NewStudentRequest.objects.all()
        return NewStudentRequest.objects.filter(student__user=user)

    def perform_create(self, serializer):
        student_profile = self.request.user.studentprofile

        # Check for existing pending requests
        pending_requests = Request.objects.filter(student=student_profile, status='Pending').exists()
        pending_apps = DormApplication.objects.filter(student=student_profile, status='PENDING').exists()
        pending_new = NewStudentRequest.objects.filter(student=student_profile, status='Pending').exists()

        if pending_requests or pending_apps or pending_new:
            from rest_framework.exceptions import ValidationError
            raise ValidationError({'detail': 'You already have a pending request. Please wait for it to be processed.'})

        serializer.save(student=student_profile)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def warden_pending(self, request):
        """
        Get pending new student applications for the warden's assigned dormitory.
        """
        try:
            # Check if user is a warden
            if not hasattr(request.user, 'wardenprofile'):
                return Response({'detail': 'User is not a warden'}, status=403)
            
            # Get warden's assigned dormitory
            warden_profile = request.user.wardenprofile
            dormitory = warden_profile.dormitories.first()
            
            if not dormitory:
                return Response({'detail': 'No dormitory assigned to this warden'}, status=404)
            
            # Get pending new student applications (DormApplication) for this dormitory
            from .models import DormApplication
            from .serializers import DormApplicationSerializer
            
            pending_applications = DormApplication.objects.filter(
                preferred_dormitory=dormitory,
                status='PENDING'
            ).select_related(
                'student',
                'student__user',
                'preferred_dormitory'
            ).order_by('-created_at')
            
            # Use serialization that matches frontend expectations
            # Frontend expects: student_username, student_id, dorm_name, room_type_preference, reason
            # DormApplication has: room_preference (needs mapping)
            
            data = []
            for app in pending_applications:
                serializer = DormApplicationSerializer(app)
                app_data = serializer.data
                # Map room_preference to room_type_preference for frontend compatibility
                app_data['room_type_preference'] = app_data.get('room_preference')
                data.append(app_data)
                
            return Response(data)
            
        except Exception as e:
            return Response({'detail': str(e)}, status=500)

