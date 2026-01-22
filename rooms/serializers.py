from rest_framework import serializers
from .models import Room, Bed


class BedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bed
        fields = '__all__'


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
