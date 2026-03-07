from django.contrib import admin
from .models import Cart, Cartitems, OrderItems, Order
# Register your models here.


class CartItemInline(admin.TabularInline):
    model = Cartitems
    extra = 0


class OrderItemsInline(admin.TabularInline):
    model = OrderItems
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['customer', 'created_at']
    inlines = [CartItemInline]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'status', 'total_amount', 'created_at']
    list_filter = ['status']
    inlines = [OrderItemsInline]
