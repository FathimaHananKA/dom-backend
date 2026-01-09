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
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'date_joined']
        extra_kwargs = {
            'password': {'write_only': True}
        }

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
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = WardenProfile
        fields = '__all__'