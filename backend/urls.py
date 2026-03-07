from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),
    path('api/products/', include('products.urls')),
    path('api/', include('orders.urls')),
    path('api/payments/', include('payments.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
