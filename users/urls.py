from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import MeView, RegisterView, AdminDashboardView, AdminUserListView, AdminVendorApprovalView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('me/', MeView.as_view(), name='me'),
    path('admin/stats/', AdminDashboardView.as_view(), name='states'),
    path('admin/users/', AdminUserListView.as_view(), name='list-users'),
    path('admin/vendors/<int:user_id>/',
         AdminVendorApprovalView.as_view(), name='approve-vendor'),
]
