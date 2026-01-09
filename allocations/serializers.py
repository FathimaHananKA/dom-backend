from rest_framework import serializers
from .models import Allocation
from rooms.models import Bed


class AllocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allocation
        fields = '__all__'

    def validate_bed(self, bed):
        if bed.is_occupied:
            raise serializers.ValidationError("This bed is already occupied.")
        return bed

    def create(self, validated_data):
        allocation = super().create(validated_data)

        # mark bed as occupied
        bed = allocation.bed
        bed.is_occupied = True
        bed.save()

        return allocation

        
class MyAccommodationSerializer(serializers.ModelSerializer):
    dormitory = serializers.CharField(source='room.dormitory.name')
    room = serializers.CharField(source='room.room_number')
    bed = serializers.CharField(source='bed.bed_number')

    class Meta:
        model = Allocation
        fields = ['dormitory', 'room', 'bed', 'allocated_at']
