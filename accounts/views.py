from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Role, User, StudentProfile, WardenProfile
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from .serializers import (
    RoleSerializer, UserSerializer, StudentProfileSerializer, 
    WardenProfileSerializer, PasswordResetRequestSerializer, 
    PasswordResetConfirmSerializer
)

class RoleViewSet(ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [AllowAny]

class IsAdminUser(IsAuthenticated):
    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.role and request.user.role.name == 'ADMIN'



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        user = self.get_object()
        user.is_active = True
        user.save()
        return Response({'status': 'user activated'})

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response({'status': 'user deactivated'})

class StudentProfileViewSet(viewsets.ModelViewSet):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

class WardenProfileViewSet(viewsets.ModelViewSet):
    queryset = WardenProfile.objects.all()
    serializer_class = WardenProfileSerializer
    permission_classes = [IsAdminUser]

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

class PasswordResetRequestView(viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetRequestSerializer

    @action(detail=False, methods=['post'])
    def request_reset(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        
        try:
            # Fix: Use .filter().first() to handle cases where 20+ users share an email
            user = User.objects.filter(email=email).first()
            if not user:
                 return Response({'message': 'If an account exists with this email, a reset link has been sent.'}, status=status.HTTP_200_OK)

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            
            # Use frontend URL (User is on 8080)
            reset_url = f"http://localhost:8080/reset-password/{uid}/{token}"
            
            message = f"Hello {user.username},\n\nYou requested a password reset. Click the link below to set a new password:\n\n{reset_url}\n\nIf you didn't request this, please ignore this email."
            
            send_mail(
                'Password Reset Request - Dormitory Management',
                message,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            return Response({'message': 'Password reset link sent to your email.'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            # Subtle response for security
            return Response({'message': 'If an account exists with this email, a reset link has been sent.'}, status=status.HTTP_200_OK)

class PasswordResetConfirmView(viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetConfirmSerializer

    @action(detail=False, methods=['post'])
    def confirm_reset(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        uidb64 = serializer.validated_data['uid']
        token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']
        
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            
            if default_token_generator.check_token(user, token):
                # Synchronize password across ALL accounts with this email
                email = user.email
                if email:
                    users_to_update = User.objects.filter(email=email)
                    for u in users_to_update:
                        u.set_password(new_password)
                        u.save()
                    count = users_to_update.count()
                else:
                    user.set_password(new_password)
                    user.save()
                    count = 1
                return Response({'message': f'Password has been reset successfully for {count} account(s).'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'error': 'Invalid link.'}, status=status.HTTP_400_BAD_REQUEST)
