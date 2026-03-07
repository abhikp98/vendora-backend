from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Cart, Product, Cartitems, Order, OrderItems
from .serializers import CartSerializer, AddToCartSerializer, OrderSerializer, OrderItemSerializer

# Create your views here.


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, created = Cart.objects.get_or_create(customer=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def post(self, request):
        serializer = AddToCartSerializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data['product_id']
            quantity = serializer.validated_data['quantity']
            try:
                product = Product.objects.get(id=product_id, is_active=True)
            except Product.DoesNotExist:
                return Response({"error": "Product does not exists"}, status=status.HTTP_404_NOT_FOUND)
            cart, created = Cart.objects.get_or_create(customer=request.user)

            cartitems, created = Cartitems.objects.get_or_create(
                cart=cart, product=product)

            if not created:
                cartitems.quantity += quantity
                cartitems.save()
            else:
                cartitems.quantity = quantity
                cartitems.save()

            return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        cart = Cart.objects.get(customer=request.user)
        cart.items.all().delete()
        return Response({"message": "Cart Deleted"}, status=status.HTTP_200_OK)


class CartItemView(APIView):

    def delete(self, request, item_id):
        try:
            Cart_item = Cartitems.objects.get(
                id=item_id, cart__customer=request.user)
            Cart_item.delete()
            return Response({'message': 'Item removed'}, status=status.HTTP_200_OK)
        except Cartitems.DoesNotExist:
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)


class OrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(
            customer=request.user).prefetch_related('items')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            cart = Cart.objects.get(customer=request.user)
        except Cart.DoesNotExist:
            return Response({"message": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        if not Cart.objects.exists():
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)
        shipping_address = request.data.get('shipping_address')
        if not shipping_address:
            return Response({'error': 'Shipping address is required'}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(
            customer=request.user,
            total_amount=cart.get_total(),
            shipping_address=shipping_address
        )

        for cart_item in cart.items.all():
            OrderItems.objects.create(
                order=order,
                product=cart_item.product,
                vendor=cart_item.product.vendor,
                quantity=cart_item.quantity,
                price=cart_item.product.price  # snapshot price at purchase time
            )

        # clear cart after order created
        cart.items.all().delete()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VendorOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # vendor sees only order items that belong to their products
        if not request.user.is_vendor():
            return Response({'error': 'Only vendors can access this'}, status=status.HTTP_403_FORBIDDEN)

        order_items = OrderItems.objects.filter(
            vendor=request.user).select_related('order', 'product')
        data = []
        for item in order_items:
            data.append({
                'order_id': item.order.id,
                'order_status': item.order.status,
                'product': item.product.name,
                'quantity': item.quantity,
                'price': str(item.price),
                'subtotal': str(item.get_subtotal()),
                'customer': item.order.customer.username,
                'shipping_address': item.order.shipping_address,
            })
        return Response(data)
