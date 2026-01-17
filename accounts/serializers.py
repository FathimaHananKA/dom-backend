from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Role, User, StudentProfile, WardenProfile

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Allow login with email or username
        identifier = attrs.get('email') or attrs.get('username')  # accept both
        password = attrs.get('password')
        if identifier and password:
            try:
                if '@' in identifier:
                    user = User.objects.get(email=identifier)
                else:
                    user = User.objects.get(username=identifier)
                if user.check_password(password) and user.is_active:
                    refresh = RefreshToken.for_user(user)
                    user_data = UserSerializer(user).data
                    return {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        'user': user_data,
                    }
                else:
                    # Temporary: allow login without password check for testing
                    if user.is_active:
                        refresh = RefreshToken.for_user(user)
                        user_data = UserSerializer(user).data
                        return {
                            'refresh': str(refresh),
                            'access': str(refresh.access_token),
                            'user': user_data,
                        }
                    else:
                        raise serializers.ValidationError('Account is not active')
            except User.DoesNotExist:
                raise serializers.ValidationError('Invalid credentials')
        return super().validate(attrs)

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    student_profile = serializers.SerializerMethodField()
    role_name = serializers.CharField(source='role.name', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'role_name', 'student_profile', 'is_active', 'date_joined']
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
            }
        return None

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
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

    class Meta:
        model = StudentProfile
        fields = '__all__'

    def create(self, validated_data):
        username = validated_data.pop('username')
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        
        user_data = {
            'username': username,
            'email': email,
            'password': password
        }
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        # Set role to STUDENT
        student_role = Role.objects.get(name='STUDENT')
        user.role = student_role
        user.save()
        
        student_profile = StudentProfile.objects.create(user=user, **validated_data)
        return student_profile

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
        
        # Remove these from validated_data as they are not model fields
        if 'first_name' in validated_data:
            validated_data.pop('first_name')
        if 'last_name' in validated_data:
            validated_data.pop('last_name')

        user_data = {
            'username': username,
            'email': email,
            'password': password,
            'first_name': first_name,
            'last_name': last_name
        }
        
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        
        # Set role to WARDEN
        try:
            warden_role = Role.objects.get(name='WARDEN')
        except Role.DoesNotExist:
             # Fallback or create if not exists
            warden_role, _ = Role.objects.get_or_create(name='WARDEN')
            
        user.role = warden_role
        user.save()
        
        warden_profile = WardenProfile.objects.create(user=user, **validated_data)
        return warden_profile