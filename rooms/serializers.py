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
        fields = ['id', 'room_number', 'dormitory', 'floor', 'room_type', 'total_beds', 'beds']

    def create(self, validated_data):
        room = Room.objects.create(**validated_data)
        # Auto-create beds
        for i in range(1, room.total_beds + 1):
            Bed.objects.create(
                bed_number=f"{room.room_number}-{chr(64+i)}", # e.g., 101-A, 101-B
                room=room
            )
        return room
