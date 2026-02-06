from rest_framework import serializers
from .models import Request, DormApplication, NewStudentRequest

class RequestSerializer(serializers.ModelSerializer):
    student_username = serializers.CharField(source='student.user.username', read_only=True)
    student_name = serializers.SerializerMethodField()
    current_dormitory_name = serializers.SerializerMethodField()
    current_room_number = serializers.SerializerMethodField()
    current_bed_number = serializers.SerializerMethodField()
    preferred_dormitory_name = serializers.SerializerMethodField()
    preferred_dormitory_id = serializers.SerializerMethodField()

    student_id = serializers.CharField(source='student.student_id', read_only=True)
    student_email = serializers.EmailField(source='student.user.email', read_only=True)
    student_phone = serializers.SerializerMethodField()
    gender = serializers.CharField(source='student.gender', read_only=True)
    department = serializers.CharField(source='student.department', read_only=True)
    allocation = serializers.SerializerMethodField()

    class Meta:
        model = Request
        fields = [
            'id', 'student', 'student_username', 'student_name', 'student_id', 
            'student_email', 'student_phone', 'gender', 'department',
            'current_room', 'current_dormitory_name', 'current_room_number', 'current_bed_number',
            'preferred_dormitory', 'preferred_dormitory_name', 'preferred_dormitory_id',
            'room_type_preference', 'preferred_room', 'reason', 
            'status', 'reviewed_at', 'requested_at',
            'warden_info', 'allocation'
        ]
        read_only_fields = ('reviewed_at', 'requested_at', 'student')
    
    warden_info = serializers.SerializerMethodField()

    def get_warden_info(self, obj):
        """Get warden info from the preferred dormitory"""
        try:
            warden = obj.preferred_dormitory.assigned_warden
            if warden:
                return {
                    'name': warden.user.get_full_name() or warden.user.username,
                    'email': warden.user.email,
                    'phone': warden.phone_number
                }
        except Exception:
            pass
        return None

    def get_allocation(self, obj):
        # Check if the student has an allocation
        try:
            from allocations.models import Allocation
            
            # Use filter().first()
            allocation = Allocation.objects.filter(student=obj.student).select_related(
                'bed', 'bed__room', 'bed__room__dormitory'
            ).first()
            
            if not allocation:
                return None

            return {
                'dormitory_id': allocation.bed.room.dormitory.id,
                'dormitory_name': allocation.bed.room.dormitory.name,
                'room_type': allocation.bed.room.room_type,
                'room_number': allocation.bed.room.room_number,
                'bed_number': allocation.bed.bed_number,
                'bed_number': allocation.bed.bed_number,
                'allocated_at': allocation.allocated_at,
                'is_paid': allocation.is_paid,
                'warden_name': allocation.bed.room.dormitory.assigned_warden.user.get_full_name() or allocation.bed.room.dormitory.assigned_warden.user.username if allocation.bed.room.dormitory.assigned_warden else 'N/A',
                'warden_email': allocation.bed.room.dormitory.assigned_warden.user.email if allocation.bed.room.dormitory.assigned_warden else 'N/A',
                'warden_phone': allocation.bed.room.dormitory.assigned_warden.phone_number if allocation.bed.room.dormitory.assigned_warden else 'N/A'
            }
        except Exception as e:
            print(f"Error serializing allocation for request {obj.id}: {str(e)}")
            return None
    
    def get_student_name(self, obj):
        """Get student's full name or username"""
        try:
            return obj.student.user.get_full_name() or obj.student.user.username
        except:
            return "Unknown"
    
    def get_student_phone(self, obj):
        """Get student's phone number"""
        return getattr(obj.student, 'phone', 'N/A')

    def get_current_dormitory_name(self, obj):
        if obj.current_room and obj.current_room.dormitory:
            return obj.current_room.dormitory.name
        return "N/A"

    def get_current_room_number(self, obj):
        if obj.current_room:
            return obj.current_room.room_number
        return "N/A"

    def get_current_bed_number(self, obj):
        if obj.current_bed_number:
            return obj.current_bed_number
        
        # Fallback for old requests
        try:
            if hasattr(obj.student, 'allocation') and obj.student.allocation:
                allocation = obj.student.allocation
                # Only return the current bed if it's in the same room recorded in the request
                if obj.current_room and allocation.bed.room == obj.current_room:
                    return allocation.bed.bed_number
        except:
            pass
        return "N/A"

    def get_preferred_dormitory_name(self, obj):
        if obj.preferred_dormitory:
            return obj.preferred_dormitory.name
        return "Any"

    def get_preferred_dormitory_id(self, obj):
        if obj.preferred_dormitory:
            return obj.preferred_dormitory.id
        return None



# Dorm Application Serializer
class DormApplicationSerializer(serializers.ModelSerializer):
    student_username = serializers.CharField(source='student.user.username', read_only=True)
    student_id = serializers.CharField(source='student.student_id', read_only=True)
    gender = serializers.CharField(source='student.gender', read_only=True)
    department = serializers.CharField(source='student.department', read_only=True)
    dorm_name = serializers.CharField(source='preferred_dormitory.name', read_only=True)
    allocation = serializers.SerializerMethodField()
    warden_info = serializers.SerializerMethodField()

    class Meta:
        model = DormApplication
        fields = [
            'id',
            'student',
            'student_username',
            'student_id',
            'gender',
            'department',
            'preferred_dormitory',
            'room_preference',
            'dorm_name',
            'status',
            'created_at',
            'allocation',
            'warden_info'
        ]
        read_only_fields = ['created_at', 'student', 'student_username', 'student_id', 'gender', 'department']

    def get_warden_info(self, obj):
        """Get warden info from the preferred dormitory"""
        try:
            warden = obj.preferred_dormitory.assigned_warden
            if warden:
                return {
                    'name': warden.user.get_full_name() or warden.user.username,
                    'email': warden.user.email,
                    'phone': warden.phone_number
                }
        except Exception:
            pass
        return None

    def get_allocation(self, obj):
        # Check if the student has an allocation
        try:
            # Import strictly inside method or at top if not circular
            from allocations.models import Allocation
            
            # Use filter().first() to avoid exceptions if not found
            allocation = Allocation.objects.filter(student=obj.student).select_related(
                'bed', 'bed__room', 'bed__room__dormitory', 'bed__room__dormitory__assigned_warden__user'
            ).first()
            
            if not allocation:
                return None
                
            return {
                'dormitory_id': allocation.bed.room.dormitory.id,
                'dormitory_name': allocation.bed.room.dormitory.name,
                'room_type': allocation.bed.room.room_type,
                'room_number': allocation.bed.room.room_number,
                'bed_number': allocation.bed.bed_number,
                'bed_number': allocation.bed.bed_number,
                'allocated_at': allocation.allocated_at,
                'is_paid': allocation.is_paid,
                'warden_name': allocation.bed.room.dormitory.assigned_warden.user.get_full_name() or allocation.bed.room.dormitory.assigned_warden.user.username if allocation.bed.room.dormitory.assigned_warden else 'N/A',
                'warden_email': allocation.bed.room.dormitory.assigned_warden.user.email if allocation.bed.room.dormitory.assigned_warden else 'N/A',
                'warden_phone': allocation.bed.room.dormitory.assigned_warden.phone_number if allocation.bed.room.dormitory.assigned_warden else 'N/A'
            }
        except Exception as e:
            print(f"Error serializing allocation for app {obj.id}: {str(e)}")
            return None


class AdminDormApplicationSerializer(DormApplicationSerializer):
    class Meta(DormApplicationSerializer.Meta):
        read_only_fields = ['created_at', 'student', 'student_username', 'student_id', 'gender', 'department']


class NewStudentRequestSerializer(serializers.ModelSerializer):
    student_username = serializers.CharField(source='student.user.username', read_only=True)
    dorm_name = serializers.CharField(source='preferred_dormitory.name', read_only=True)

    student_id = serializers.CharField(source='student.student_id', read_only=True)
    gender = serializers.CharField(source='student.gender', read_only=True)

    class Meta:
        model = NewStudentRequest
        fields = '__all__'
        read_only_fields = ('created_at', 'student')
