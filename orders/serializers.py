from rest_framework import serializers
from products.serializers import ProductSerializer
from .models import Cartitems, Cart, Order, OrderItems


class CartItemSerializer(serializers.ModelSerializer):
    product_detail = ProductSerializer(source='product', read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = Cartitems
        fields = ['id', 'product', 'product_detail', 'quantity', 'subtotal']

    def get_subtotal(self, obj):
        return obj.get_subtotal()


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total']

    def get_total(self, obj):
        return obj.get_total()


class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1, default=1)


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = OrderItems
        fields = ['id', 'product_name', 'quantity', 'price', 'subtotal']

    def get_subtotal(self, obj):
        return obj.get_subtotal()


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'status', 'total_amount',
                  'shipping_address', 'items', 'created_at']
        read_only_fields = ['status', 'total_amount']
        
