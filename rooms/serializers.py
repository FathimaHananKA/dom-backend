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
        fields = '__all__'
