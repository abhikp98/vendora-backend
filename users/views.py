from .serializers import *
from .models import User
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from orders.models import Order
from django.db import models
from .serializers import UserSerialiser
# Create your views here.


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Account Created Successfully",
                "user": UserSerialiser(user).data,
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token)
                },

            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerialiser(request.user)
        print(serializer.data)
        return Response(serializer.data)


class AdminDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_admin():
            return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
        total_users = User.objects.filter(role=User.CUSTOMER).count()
        total_vendors = User.objects.filter(role=User.VENDOR).count()
        total_orders = Order.objects.count()
        total_revenue = Order.objects.filter(
            status=Order.CONFIRMED
        ).aggregate(
            total=models.Sum('total_amount')
        )['total'] or 0
        return Response({
            'total_users': total_users,
            'total_vendors': total_vendors,
            'total_orders': total_orders,
            'total_revenue': total_revenue,
        })


class AdminUserListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_admin():
            return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)

        role = request.query_params.get('role', None)
        users = User.objects.exclude(id=request.user.id)
        if role:
            users = users.filter(role=role)
        serializer = UserSerialiser(users, many=True)
        return Response(serializer.data)


class AdminVendorApprovalView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        if not request.user.is_admin():
            return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)

        try:
            vendor = User.objects.get(id=user_id, role=User.VENDOR)
        except User.DoesNotExist:
            return Response({'error': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)

        action = request.data.get('action')
        if action == 'approve':
            vendor.is_active = True
            vendor.save()
            return Response({'message': 'Vendor approved'})
        elif action == 'reject':
            vendor.is_active = False
            vendor.save()
            return Response({'message': 'Vendor rejected'})

        return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
