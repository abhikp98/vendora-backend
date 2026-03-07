from rest_framework import serializers
from .models import Product, ProductImages, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = ['id', 'image', 'is_primary']


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    category_name = serializers.CharField(
        source='category.name', read_only=True)

    vendor_name = serializers.CharField(
        source='vendor.username', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'price',
            'stock', 'is_active', 'category', 'category_name',
            'vendor', 'vendor_name', 'images', 'created_at'
        ]

    read_only_fields = ['vendor', 'created_at']


class ProductCreateSerializer(serializers.ModelSerializer):
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )

    class Meta:
        model = Product
        fields = ['name', 'description', 'price',
                  'stock', 'category', 'uploaded_images']

        read_only_fields = ['vendor']

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        product = Product.objects.create(**validated_data)
        for index, image in enumerate(uploaded_images):
            ProductImages.objects.create(
                product=product,
                image=image,
                is_primary=(index == 0)
            )
        return product
