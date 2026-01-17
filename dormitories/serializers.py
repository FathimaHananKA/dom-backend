from rest_framework import serializers
from .models import Dormitory

class DormitorySerializer(serializers.ModelSerializer):
    warden_name = serializers.CharField(source='assigned_warden.user.username', read_only=True)
    
    class Meta:
        model = Dormitory
        fields = ['id', 'name', 'gender', 'total_rooms', 'total_beds', 'assigned_warden', 'warden_name']
