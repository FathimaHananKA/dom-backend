from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'amount', 'razorpay_order_id', 'status', 'created_at')
    search_fields = ('razorpay_order_id', 'razorpay_payment_id', 'student__user__username')
    list_filter = ('status', 'created_at')
