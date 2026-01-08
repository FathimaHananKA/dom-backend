from rest_framework import serializers
from .models import Request

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = '__all__'
        read_only_fields = ('status', 'reviewed_at', 'requested_at')
