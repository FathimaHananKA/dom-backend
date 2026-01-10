from rest_framework.viewsets import ModelViewSet
from rest_framework import generics, permissions
from .models import Request, DormApplication
from .serializers import RequestSerializer, DormApplicationSerializer

# Existing Room Change Requests
class RequestViewSet(ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer


# Dorm Application Views

class DormApplicationCreateView(generics.CreateAPIView):
    """
    Allow a student to apply for a dormitory.
    """
    serializer_class = DormApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically assign the logged-in student
        serializer.save(student=self.request.user.studentprofile)


class DormApplicationDetailView(generics.RetrieveAPIView):
    """
    Retrieve the current logged-in student's dorm application.
    """
    serializer_class = DormApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Return the dorm application for the logged-in student
        student_profile = self.request.user.studentprofile
        # There should be only one active application per student
        return DormApplication.objects.filter(student=student_profile).first()
