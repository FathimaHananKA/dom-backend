from rest_framework import serializers
from .models import Allocation
from rooms.models import Bed


class AllocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allocation
        fields = '__all__'

    def validate_bed(self, bed):
        # Check if bed is occupied AND has an active allocation
        if bed.is_occupied:
            # Self-healing: If marked occupied but NO allocation exists, allow it.
            if Allocation.objects.filter(bed=bed).exists():
                raise serializers.ValidationError("This bed is already occupied.")
            else:
                # If no allocation, we effectively consider it available and allow re-allocation
                # We could auto-fix here, but create() will set it to True anyway.
                pass
        return bed

    def create(self, validated_data):
        allocation = super().create(validated_data)
        # mark bed as occupied
        bed = allocation.bed
        bed.is_occupied = True
        bed.save()
        return allocation

    def update(self, instance, validated_data):
        old_bed = instance.bed
        new_bed = validated_data.get('bed', old_bed)

        if old_bed != new_bed:
            old_bed.is_occupied = False
            old_bed.save()

            new_bed.is_occupied = True
            new_bed.save()

        return super().update(instance, validated_data)

        
class MyAccommodationSerializer(serializers.ModelSerializer):
    dormitory = serializers.CharField(source='room.dormitory.name')
    room = serializers.CharField(source='room.room_number')
    bed = serializers.CharField(source='bed.bed_number')

    class Meta:
        model = Allocation
        fields = ['dormitory', 'room', 'bed', 'allocated_at']


class AllocationListSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.user.username', read_only=True)
    student_id = serializers.CharField(source='student.student_id', read_only=True) 
    dormitory_name = serializers.CharField(source='bed.room.dormitory.name', read_only=True)
    room_number = serializers.CharField(source='bed.room.room_number', read_only=True)
    bed_number = serializers.CharField(source='bed.bed_number', read_only=True)
    room_type = serializers.CharField(source='bed.room.room_type', read_only=True)
    floor = serializers.IntegerField(source='bed.room.floor', read_only=True)
    
    class Meta:
        model = Allocation
        fields = ['id', 'student', 'bed', 'student_name', 'student_id', 'dormitory_name', 'room_number', 'bed_number', 'allocated_at', 'room_type', 'floor']
