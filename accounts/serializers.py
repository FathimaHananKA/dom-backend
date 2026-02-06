from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Role, User, StudentProfile, WardenProfile
from django.db import models
from django.db.models import Q

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        print("\n" + "="*50)
        print("DEBUG LOGIN (v4.2) STARTED")
        print("="*50)
        
        raw_identifier = attrs.get('email') or attrs.get('username') or ""
        identifier = str(raw_identifier).strip()
        password = str(attrs.get('password') or "")
        
        print(f"IDENTIFIER PROVIDED: {repr(identifier)}")
        print(f"PASSWORD PROVIDED: [HIDDEN] (Length: {len(password)})")

        if not identifier or not password:
            print("FAILED: Missing identifier or password")
            raise serializers.ValidationError({'detail': 'Please provide both username/email and password.'})

        # Find all users matching the identifier (email or username)
        candidates = User.objects.filter(Q(email=identifier) | Q(username=identifier))
        print(f"FOUND {candidates.count()} CANDIDATE(S)")

        found_user = None
        has_inactive_match = False
        
        for i, user in enumerate(candidates):
            pw_match = user.check_password(password)
            print(f"Checking Candidate {i+1}: {user.username} (ID: {user.id})")
            print(f"  - Password Match: {pw_match}")
            print(f"  - Is Active: {user.is_active}")
            
            if pw_match:
                if user.is_active:
                    found_user = user
                    print("  - [SUCCESS] Active matching user found!")
                    break
                else:
                    has_inactive_match = True
                    print("  - [FAILED] Match found but user is inactive")
        
        if found_user:
            print(f"LOGIN APPROVED FOR: {found_user.username}")
            refresh = RefreshToken.for_user(found_user)
            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(found_user).data,
            }
        
        if not candidates.exists():
            print("FAILED: No account exists with that identifier.")
            raise serializers.ValidationError({'detail': f'ERROR_CODE_1: No account exists for: {identifier}'})
        
        if has_inactive_match:
            print("FAILED: Match found but it is inactive.")
            raise serializers.ValidationError({'detail': 'ERROR_CODE_2: Your account is currently inactive.'})
            
        print("FAILED: All candidates failed password check.")
        raise serializers.ValidationError({'detail': f'ERROR_CODE_3: Incorrect password for {identifier}. Try resetting it.'})

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    student_profile = serializers.SerializerMethodField()
    role_name = serializers.CharField(source='role.name', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'role', 'role_name', 'student_profile', 'is_active', 'date_joined']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def get_student_profile(self, obj):
        if hasattr(obj, 'studentprofile'):
            return {
                'student_id': obj.studentprofile.student_id,
                'department': obj.studentprofile.department,
                'year': obj.studentprofile.year,
                'gender': obj.studentprofile.gender,
                'can_change_room': obj.studentprofile.can_change_room,
            }
        return None

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

class StudentProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    user = UserSerializer(read_only=True)

    status = serializers.SerializerMethodField()
    payment_status = serializers.SerializerMethodField()

    class Meta:
        model = StudentProfile
        fields = '__all__'

    def get_status(self, obj):
        try:
            from student_requests.models import DormApplication, NewStudentRequest, Request
            app = DormApplication.objects.filter(student=obj).order_by('-created_at').first()
            if app:
                return app.status.capitalize()
            new_req = NewStudentRequest.objects.filter(student=obj).order_by('-created_at').first()
            if new_req:
                return new_req.status
            room_req = Request.objects.filter(student=obj).order_by('-requested_at').first()
            if room_req:
                return room_req.status
            return 'Pending'
        except Exception:
            return 'Pending'

    def get_payment_status(self, obj):
        try:
            from payments.models import Payment
            payment_exists = Payment.objects.filter(student=obj, status='SUCCESS').exists()
            return 'Paid' if payment_exists else 'Pending'
        except Exception:
            return 'Pending'

    def create(self, validated_data):
        username = validated_data.pop('username')
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        
        user_data = {'username': username, 'email': email, 'password': password}
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        
        student_role = Role.objects.get(name='STUDENT')
        user.role = student_role
        user.save()
        
        return StudentProfile.objects.create(user=user, **validated_data)

class WardenProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    username = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = WardenProfile
        fields = ['id', 'user', 'employee_id', 'phone_number', 'username', 'email', 'password', 'first_name', 'last_name', 'gender']
        
    def create(self, validated_data):
        username = validated_data.pop('username')
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        first_name = validated_data.get('first_name', '')
        last_name = validated_data.get('last_name', '')
        
        if 'first_name' in validated_data: validated_data.pop('first_name')
        if 'last_name' in validated_data: validated_data.pop('last_name')

        user_data = {
            'username': username, 'email': email, 'password': password,
            'first_name': first_name, 'last_name': last_name
        }
        
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        
        warden_role, _ = Role.objects.get_or_create(name='WARDEN')
        user.role = warden_role
        user.save()
        
        return WardenProfile.objects.create(user=user, **validated_data)

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, min_length=8)
    token = serializers.CharField()
    uid = serializers.CharField()