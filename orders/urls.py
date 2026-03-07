from django.urls import path
from .views import CartView, CartItemView, OrderView, VendorOrderView

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/<int:item_id>/', CartItemView.as_view(), name='cart-item'),
    path('orders/', OrderView.as_view(), name='orders'),
    path('vendor/orders/', VendorOrderView.as_view(), name='vendor-orders'),

]
