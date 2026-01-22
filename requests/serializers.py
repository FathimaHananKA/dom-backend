from rest_framework import serializers
from .models import Request,DormApplication

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = '__all__'
        read_only_fields = ('status', 'reviewed_at', 'requested_at')



# Dorm Application Serializer
class DormApplicationSerializer(serializers.ModelSerializer):
    student_username = serializers.CharField(source='student.user.username', read_only=True)
    student_id = serializers.CharField(source='student.student_id', read_only=True)
    gender = serializers.CharField(source='student.gender', read_only=True)
    department = serializers.CharField(source='student.', read_only=True)
    dorm_name = serializers.CharField(source='preferred_dormitory.name', read_only=True)

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
            'created_at'
        ]
        read_only_fields = ['status', 'created_at', 'student', 'student_username', 'student_id', 'gender', 'department']