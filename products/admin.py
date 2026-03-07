from django.contrib import admin
from .models import Product, ProductImages, Category

# Register your models here.


class ProductImageInline(admin.TabularInline):
    extra = 1
    model = ProductImages


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'vendor', 'category',
                    'price', 'stock', 'is_active']
    list_filter = ['is_active', 'category']
    prepopulated_fields = {'slug': ('name', )}
    inlines = [ProductImageInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
