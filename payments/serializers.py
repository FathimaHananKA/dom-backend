from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class PaymentDetailSerializer(serializers.ModelSerializer):
    # Student Information
    student_name = serializers.SerializerMethodField()
    student_id = serializers.SerializerMethodField()
    student_email = serializers.SerializerMethodField()
    student_phone = serializers.SerializerMethodField()
    student_year = serializers.SerializerMethodField()
    student_course = serializers.SerializerMethodField()
    
    # Allocation Information
    dormitory_name = serializers.SerializerMethodField()
    room_number = serializers.SerializerMethodField()
    room_type = serializers.SerializerMethodField()
    bed_number = serializers.SerializerMethodField()
    
    # Warden Information
    warden_name = serializers.SerializerMethodField()
    warden_email = serializers.SerializerMethodField()
    warden_phone = serializers.SerializerMethodField()
    
    class Meta:
        model = Payment
        fields = [
            'id', 'amount', 'currency', 'status',
            'razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature',
            'created_at', 'updated_at',
            # Student fields
            'student_name', 'student_id', 'student_email', 'student_phone',
            'student_year', 'student_course',
            # Allocation fields
            'dormitory_name', 'room_number', 'room_type', 'bed_number',
            # Warden fields
            'warden_name', 'warden_email', 'warden_phone'
        ]
    
    def get_student_name(self, obj):
        user = obj.student.user
        return user.get_full_name() or user.username
    
    def get_student_id(self, obj):
        return obj.student.student_id
    
    def get_student_email(self, obj):
        return obj.student.user.email
    
    def get_student_phone(self, obj):
        return getattr(obj.student, 'phone', '')
    
    def get_student_year(self, obj):
        return obj.student.year
    
    def get_student_course(self, obj):
        return getattr(obj.student, 'course', 'N/A')
    
    def get_dormitory_name(self, obj):
        if obj.allocation and obj.allocation.bed:
            return obj.allocation.bed.room.dormitory.name
        return None
    
    def get_room_number(self, obj):
        if obj.allocation and obj.allocation.bed:
            return obj.allocation.bed.room.room_number
        return None
    
    def get_room_type(self, obj):
        if obj.allocation and obj.allocation.bed:
            return obj.allocation.bed.room.room_type
        return None
    
    def get_bed_number(self, obj):
        if obj.allocation and obj.allocation.bed:
            return obj.allocation.bed.bed_number
        return None
    
    def get_warden_name(self, obj):
        if obj.allocation and obj.allocation.bed:
            warden = obj.allocation.bed.room.dormitory.assigned_warden
            if warden:
                return warden.user.get_full_name() or warden.user.username
        return None
    
    def get_warden_email(self, obj):
        if obj.allocation and obj.allocation.bed:
            warden = obj.allocation.bed.room.dormitory.assigned_warden
            if warden:
                return warden.user.email
        return None
    
    def get_warden_phone(self, obj):
        if obj.allocation and obj.allocation.bed:
            warden = obj.allocation.bed.room.dormitory.assigned_warden
            if warden:
                return getattr(warden, 'phone_number', '')
        return None
