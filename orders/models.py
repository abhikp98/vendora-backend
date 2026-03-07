from django.db import models
from users.models import User
from products.models import Product

# Create your models here.


class Cart(models.Model):
    customer = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"cart of {self.customer.username}"

    def get_total(self):
        return sum(item.get_subtotal() for item in self.items.all())


class Cartitems(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_subtotal(self):
        # price x quantity for this item
        return self.product.price * self.quantity


class Order(models.Model):
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'

    STATUS_CHOICE = [
        (PENDING, 'Pending'),
        (CONFIRMED, 'Confirmed'),
        (SHIPPED, 'Shipped'),
        (DELIVERED, 'Delivered'),
        (CANCELLED, 'Cancelled'),
    ]

    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(choices=STATUS_CHOICE,
                              max_length=40, default=PENDING)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updates_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} by {self.customer.username}"
    
    class Meta:
        ordering = ['-created_at']


class OrderItems(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    vendor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_subtotal(self):
        return self.price * self.quantity
