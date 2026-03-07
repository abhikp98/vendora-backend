from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.


@admin.register(User)
class CustomuserAdmin(UserAdmin):
    list_display = ['username', 'email', 'role', 'is_active', 'date_joined']
    list_filter = ['role', 'is_active']
    fieldsets = UserAdmin.fieldsets+(
        ('Custom Fields', {'fields': ('role', 'phone', 'profile_picture')}),
    )
