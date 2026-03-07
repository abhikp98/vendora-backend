from django.urls import path
from .views import CategoryListView, ProductListView, ProductDetailView, VendorProductView, VendorProductDetailView


urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('', ProductListView.as_view(), name='products'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product_details'),
    path('vendor/products/', VendorProductView.as_view(), name='vendor-products'),
    path('vendor/products/<slug:slug>/',
         VendorProductDetailView.as_view(), name='vendor-product-detail'),
]
