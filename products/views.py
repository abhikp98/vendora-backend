from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer, ProductCreateSerializer
from rest_framework import status
# Create your views here.


class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    permission_classes = [AllowAny]
    model = Category
    serializer_class = CategorySerializer


class ProductListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        products = Product.objects.filter(is_active=True).select_related(
            'vendor', 'category').prefetch_related('images')
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, slug):
        try:
            product = Product.objects.get(slug=slug, is_active=True)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)


class VendorProductView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = Product.objects.filter(vendor=request.user)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_vendor():
            return Response({'error': 'Only vendors can create products'}, status=status.HTTP_403_FORBIDDEN)

        serializer = ProductCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(vendor=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendorProductDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, request, slug, user):
        try:
            return Product.objects.get(slug=slug, vendor=user)
        except Product.DoesNotExist:
            return None

    def put(self, request, slug):
        product = self.get_object(slug, request.user)
        if not product:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductCreateSerializer(
            product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        product = self.get_object(slug, request.user)
        if not product:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return Response({'message': 'Product deleted'}, status=status.HTTP_204_NO_CONTENT)
