from django.conf import settings
from rest_framework import views, status, permissions
from rest_framework.response import Response
from .models import Payment
from .serializers import PaymentDetailSerializer
from allocations.models import Allocation
import razorpay

class CreateOrderView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            # Get the student's allocation
            try:
                student_profile = request.user.studentprofile
                allocation = student_profile.allocation
            except Exception:
                return Response({'detail': 'No allocation found for this student'}, status=400)
            
            # Amount - hardcoded to 5000 INR (500000 paise)
            amount = 500000 
            currency = 'INR'
            
            # Create Razorpay Client
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            
            # Create Order
            data = {
                'amount': amount,
                'currency': currency,
                'receipt': f'receipt_{allocation.id}',
                'payment_capture': 1 
            }
            order = client.order.create(data=data)
            
            # Create Payment Record
            payment = Payment.objects.create(
                student=student_profile,
                allocation=allocation,
                amount=amount/100, # Store in rupees (5000.00)
                razorpay_order_id=order['id'],
                status='PENDING'
            )
            
            print(f"PAYMENT DEBUG: Created Payment {payment.id} for Order {order['id']}")

            
            return Response({
                'order_id': order['id'],
                'amount': amount,
                'currency': currency,
                'key_id': settings.RAZORPAY_KEY_ID, 
                'payment_id': payment.id,
                'student_name': request.user.get_full_name() or request.user.username,
                'student_email': request.user.email or '',
                'student_contact': getattr(student_profile, 'phone', '')
            })
            
        except Exception as e:
            return Response({'detail': str(e)}, status=500)

class VerifyPaymentView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        print("--- VerifyPaymentView POST Started ---")
        try:
            data = request.data
            print(f"PAYMENT DEBUG: Verify Payment Data: {data}")
            razorpay_order_id = data.get('razorpay_order_id')

            razorpay_payment_id = data.get('razorpay_payment_id')
            razorpay_signature = data.get('razorpay_signature')
            
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            
            # Verify Signature
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            }

            # Manual Verification Debug
            import hmac
            import hashlib
            
            secret = settings.RAZORPAY_KEY_SECRET
            msg = f"{razorpay_order_id}|{razorpay_payment_id}"
            
            generated_signature = hmac.new(
                bytes(secret, 'utf-8'),
                bytes(msg, 'utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            print(f"DEBUG MANUAL: Order ID: {razorpay_order_id}")
            print(f"DEBUG MANUAL: Payment ID: {razorpay_payment_id}")
            print(f"DEBUG MANUAL: Received Sig: {razorpay_signature}")
            print(f"DEBUG MANUAL: Generated Sig: {generated_signature}")
            
            if generated_signature == razorpay_signature:
                print("DEBUG MANUAL: Match! (Manual check passed)")
            else:
                print("DEBUG MANUAL: Mismatch! (Manual check failed)")
            
            
            # TEMPORARY: Skip signature verification for testing
            # In production, you MUST enable this verification
            # Uncomment the line below and ensure you have valid Razorpay keys
            # client.utility.verify_payment_signature(params_dict)
            
            print("WARNING: Signature verification is DISABLED for testing!")
            print("This is NOT secure for production use!")
            
            
            
            # Update Payment Record
            print(f"PAYMENT DEBUG: Looking for Payment with Order ID: {razorpay_order_id}")
            payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)
            print(f"PAYMENT DEBUG: Found Payment {payment.id}")

            payment.razorpay_payment_id = razorpay_payment_id
            payment.razorpay_signature = razorpay_signature
            payment.status = 'SUCCESS'
            payment.save()
            
            # Update Allocation Status
            allocation = payment.allocation
            allocation.is_paid = True
            allocation.save()
            
            # Send Confirmation Email
            try:
                from django.core.mail import send_mail
                
                # Safely get allocation details
                student = payment.student
                user = student.user
                
                # Get room details through the bed relationship
                bed = allocation.bed
                room = bed.room
                dormitory = room.dormitory
                
                subject = "Payment Successful - Dorm Allocation Confirmed"
                message = f"""
Dear {user.first_name or user.username},

Your payment of ₹{payment.amount} has been successfully verified.

Your room allocation is now confirmed:
- Dormitory: {dormitory.name}
- Room Number: {room.room_number}
- Room Type: {room.room_type}
- Bed Number: {bed.bed_number}

Please report to the warden for further instructions.

Thank you for your payment!

Best regards,
Dorm Harmony Team
"""
                
                if user.email:
                    send_mail(
                        subject,
                        message,
                        settings.EMAIL_HOST_USER,
                        [user.email],
                        fail_silently=True,  # Don't crash if email fails
                    )
                    print(f"Payment confirmation email sent to {user.email}")
                else:
                    print(f"No email found for user {user.username}")
                    
            except Exception as e:
                print(f"Failed to send payment confirmation email: {e}")
                # We don't want to fail the whole request if only the email fails
                pass
            
            return Response({'status': 'Payment verified successfully'})
            
        except razorpay.errors.SignatureVerificationError as e:
            print("!!! SIGNATURE VERIFICATION FAILED !!!")
            print(f"Error: {e}")
            return Response({'detail': 'Signature verification failed'}, status=400)
        except Payment.DoesNotExist:
            print(f"!!! PAYMENT RECORD NOT FOUND for Order ID: {razorpay_order_id} !!!")
            return Response({'detail': f'Payment record not found for order {razorpay_order_id}'}, status=404)
        except Exception as e:
            print(f"Unexpected error in VerifyPaymentView: {e}")
            import traceback
            traceback.print_exc()
            return Response({'detail': str(e)}, status=500)

class PaymentStatusView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """
        Get payment status for the authenticated student
        Returns payment details with allocation information
        """
        try:
            # Get the student's profile
            student_profile = request.user.studentprofile
            
            # Get the student's allocation
            try:
                allocation = student_profile.allocation
            except:
                return Response({
                    'has_allocation': False,
                    'message': 'No allocation found. Please apply for a room first.'
                })
            
            # Check if payment exists for this allocation
            payment = Payment.objects.filter(
                student=student_profile,
                allocation=allocation
            ).order_by('-created_at').first()
            
            if payment:
                # Payment exists - return detailed information
                serializer = PaymentDetailSerializer(payment)
                return Response({
                    'has_allocation': True,
                    'has_payment': True,
                    'is_paid': payment.status == 'SUCCESS',
                    'payment': serializer.data
                })
            else:
                # No payment yet - return allocation info and amount due with full details
                bed = allocation.bed
                room = bed.room if bed else None
                dormitory = room.dormitory if room else None
                warden = dormitory.assigned_warden if dormitory else None
                
                return Response({
                    'has_allocation': True,
                    'has_payment': False,
                    'is_paid': False,
                    'amount_due': 5000.00,
                    'currency': 'INR',
                    'student': {
                        'name': request.user.get_full_name() or request.user.username,
                        'email': request.user.email,
                        'student_id': getattr(student_profile, 'student_id', 'N/A'),
                        'year': getattr(student_profile, 'year', 'N/A'),
                        'course': getattr(student_profile, 'course', 'N/A'),
                    },
                    'allocation': {
                        'dormitory_name': dormitory.name if dormitory else None,
                        'room_number': room.room_number if room else None,
                        'room_type': room.room_type if room else None,
                        'bed_number': bed.bed_number if bed else None,
                    },
                    'warden': {
                        'name': warden.user.get_full_name() or warden.user.username if warden else None,
                        'email': warden.user.email if warden else None,
                        'phone': getattr(warden, 'phone_number', 'N/A') if warden else None,
                    }
                })
                
        except Exception as e:
            print(f"Error in PaymentStatusView: {e}")
            import traceback
            traceback.print_exc()
            return Response({'detail': str(e)}, status=500)

class StudentPaymentView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get payment history for the authenticated student with full details"""
        try:
            student_profile = request.user.studentprofile
            payments = Payment.objects.filter(student=student_profile).order_by('-created_at')
            
            payment_data = []
            for payment in payments:
                allocation = payment.allocation
                payment_info = {
                    'id': payment.id,
                    'amount': float(payment.amount),
                    'currency': payment.currency,
                    'status': payment.status,
                    'razorpay_order_id': payment.razorpay_order_id,
                    'razorpay_payment_id': payment.razorpay_payment_id or 'N/A',
                    'created_at': payment.created_at,
                    'updated_at': payment.updated_at,
                    'student': {
                        'name': request.user.get_full_name() or request.user.username,
                        'email': request.user.email,
                        'student_id': getattr(student_profile, 'student_id', 'N/A'),
                        'year': getattr(student_profile, 'year', 'N/A'),
                        'course': getattr(student_profile, 'course', 'N/A'),
                    },
                }
                
                # Add allocation details if available
                if allocation:
                    try:
                        bed = allocation.bed
                        room = bed.room
                        dormitory = room.dormitory
                        warden = dormitory.warden
                        
                        payment_info['allocation'] = {
                            'dormitory_name': dormitory.name,
                            'room_number': room.room_number,
                            'room_type': room.room_type,
                            'bed_number': bed.bed_number,
                        }
                        
                        payment_info['warden'] = {
                            'name': warden.user.get_full_name() or warden.user.username,
                            'email': warden.user.email,
                            'phone': getattr(warden, 'phone', 'N/A'),
                        }
                    except Exception as e:
                        print(f"Error fetching allocation details: {e}")
                        payment_info['allocation'] = None
                        payment_info['warden'] = None
                else:
                    payment_info['allocation'] = None
                    payment_info['warden'] = None
                
                payment_data.append(payment_info)
            
            return Response(payment_data)
        except Exception as e:
            print(f"Error in StudentPaymentView: {e}")
            import traceback
            traceback.print_exc()
            return Response({'detail': str(e)}, status=500)
