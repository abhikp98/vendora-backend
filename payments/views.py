import razorpay
from backend import settings
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from orders.models import Order
from rest_framework.response import Response
from rest_framework import status

# initialize razorpay


class CreatePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        try:

            order = Order.objects.get(id=order_id, customer=request.user)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        if order.status != Order.PENDING:
            return Response({'error': 'Order already paid'}, status=status.HTTP_400_BAD_REQUEST)
        amount_in_paisa = float(order.total_amount*100)

        # create razorpay order
        razorpay_order = client.order.create({
            'amount': amount_in_paisa,
            'currency': 'INR',
            'receipt': f'order_{order.id}',
            'payment_capture': 1

        })

        return Response({

            'razorpay_order_id': razorpay_order['id'],
            'amount': amount_in_paisa,
            'currency': 'INR',
            'key': settings.RAZORPAY_KEY_ID,  # frontend needs this to open popup
            'order_id': order.id,
        }
        )


class VerifyPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, customer=request.user)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

        razorpay_order_id = request.data.get('razorpay_order_id')
        razorpay_payment_id = request.data.get('razorpay_payment_id')
        razorpay_signature = request.data.get('razorpay_signature')

        # verify signature to confirm payment is genuine
        params = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }
        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        try:
            client.utility.verify_payment_signature(params)
            order.status = Order.CONFIRMED
            order.save()
            return Response({'message': 'Payment successful', 'order_id': order.id})
        except razorpay.errors.SignatureVerificationError:
            return Response({'error': 'Payment verification failed'}, status=status.HTTP_400_BAD_REQUEST)
