from rest_framework import serializers
from .models import Dormitory

class DormitorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Dormitory
        fields = '__all__'
