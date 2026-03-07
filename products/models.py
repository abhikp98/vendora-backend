from django.db import models
from users.models import User
from django.utils.text import slugify
import uuid

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    vendor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='product')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="products")
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{uuid.uuid4().hex[:6]}"
            self.slug = slug

        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductImages(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.product.name}"
