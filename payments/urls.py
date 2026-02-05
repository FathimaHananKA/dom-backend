from django.urls import path
from .views import CreateOrderView, VerifyPaymentView, StudentPaymentView, PaymentStatusView

urlpatterns = [
    path('create-order/', CreateOrderView.as_view(), name='create-order'),
    path('verify/', VerifyPaymentView.as_view(), name='verify-payment'),
    path('my-payments/', StudentPaymentView.as_view(), name='my-payments'),
    path('status/', PaymentStatusView.as_view(), name='payment-status'),
]
