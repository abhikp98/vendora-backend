from django.urls import path
from .views import CreatePaymentView, VerifyPaymentView

urlpatterns = [
    path('create/<int:order_id>/', CreatePaymentView.as_view(), name='create'),
    path('verify/<int:order_id>/', VerifyPaymentView.as_view(), name='verify'),

]
