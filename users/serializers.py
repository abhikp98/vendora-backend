from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password',
                  'confirm_password', 'role', 'phone']

    def validate(self, attrs):

        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        if attrs['role'] == User.ADMIN:
            raise serializers.ValidationError("can't register as ADMIN")

        return attrs
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user
    

class UserSerialiser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'phone', 'profile_picture']