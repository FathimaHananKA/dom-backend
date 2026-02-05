from rest_framework import serializers
from .models import Room, Bed


class BedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bed
        fields = '__all__'


class BedWithStudentSerializer(serializers.ModelSerializer):
    """Serializer for beds with student allocation information"""
    student_name = serializers.SerializerMethodField()
    student_id = serializers.SerializerMethodField()
    allocated_at = serializers.SerializerMethodField()
    
    class Meta:
        model = Bed
        fields = ['id', 'bed_number', 'is_occupied', 'student_name', 'student_id', 'allocated_at']
    
    def get_student_name(self, obj):
        try:
            if hasattr(obj, 'allocation'):
                return obj.allocation.student.user.get_full_name() or obj.allocation.student.user.username
            return None
        except Exception:
            return None
    
    def get_student_id(self, obj):
        try:
            if hasattr(obj, 'allocation'):
                return obj.allocation.student.student_id
            return None
        except Exception:
            return None
    
    def get_allocated_at(self, obj):
        try:
            if hasattr(obj, 'allocation'):
                return obj.allocation.allocated_at
            return None
        except Exception:
            return None


class StudentInfoSerializer(serializers.Serializer):
    """Serializer for student information in occupied beds"""
    student_id = serializers.CharField()
    student_name = serializers.CharField()
    email = serializers.EmailField()
    phone = serializers.CharField()


class DetailedBedSerializer(serializers.ModelSerializer):
    """Detailed bed serializer with student information"""
    student = serializers.SerializerMethodField()
    
    class Meta:
        model = Bed
        fields = ['id', 'bed_number', 'is_occupied', 'student']
    
    def get_student(self, obj):
        """Get student information if bed is occupied"""
        if obj.is_occupied and hasattr(obj, 'allocation'):
            student_profile = obj.allocation.student
            return {
                'student_id': student_profile.student_id,
                'student_name': student_profile.user.get_full_name() or student_profile.user.username,
                'email': student_profile.user.email,
                'phone': getattr(student_profile, 'phone', 'N/A')
            }
        return None


class RoomSerializer(serializers.ModelSerializer):
    beds = BedSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ['id', 'room_number', 'dormitory', 'room_type', 'capacity', 'beds']
        
    def create(self, validated_data):
        room = Room.objects.create(**validated_data)
        # Auto-create beds based on capacity
        capacity = validated_data.get('capacity', 0)
        for i in range(1, capacity + 1):
            Bed.objects.create(
                bed_number=f"{room.room_number}-{i}",
                room=room,
                is_occupied=False
            )
        return room


class WardenRoomDetailSerializer(serializers.ModelSerializer):
    """Detailed room serializer for warden dashboard with occupancy information"""
    beds = BedWithStudentSerializer(many=True, read_only=True)
    dormitory_name = serializers.CharField(source='dormitory.name', read_only=True)
    occupied_beds = serializers.SerializerMethodField()
    total_beds = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    
    class Meta:
        model = Room
        fields = [
            'id', 'room_number', 'dormitory', 'dormitory_name', 
            'floor', 'room_type', 'capacity', 'beds', 
            'occupied_beds', 'total_beds', 'status'
        ]
    
    def get_occupied_beds(self, obj):
        return obj.beds.filter(is_occupied=True).count()
    
    def get_total_beds(self, obj):
        return obj.beds.count()
    
    def get_status(self, obj):
        occupied = obj.beds.filter(is_occupied=True).count()
        total = obj.beds.count()
        if occupied == 0:
            return 'available'
        elif occupied < total:
            return 'partial'
        else:
            return 'occupied'


class DetailedRoomSerializer(serializers.ModelSerializer):
    """Detailed room serializer for warden dashboard with occupancy info"""
    beds = DetailedBedSerializer(many=True, read_only=True)
    occupied_beds = serializers.SerializerMethodField()
    available_beds = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    dormitory_name = serializers.CharField(source='dormitory.name', read_only=True)
    
    class Meta:
        model = Room
        fields = [
            'id', 'room_number', 'dormitory', 'dormitory_name', 
            'floor', 'room_type', 'capacity', 'beds', 
            'occupied_beds', 'available_beds', 'status'
        ]
    
    def get_occupied_beds(self, obj):
        """Count occupied beds"""
        return obj.beds.filter(is_occupied=True).count()
    
    def get_available_beds(self, obj):
        """Count available beds"""
        return obj.beds.filter(is_occupied=False).count()
    
    def get_status(self, obj):
        """Determine room status based on occupancy"""
        occupied = obj.beds.filter(is_occupied=True).count()
        total = obj.capacity
        
        if occupied == 0:
            return 'available'
        elif occupied < total:
            return 'partial'
        else:
            return 'occupied'
