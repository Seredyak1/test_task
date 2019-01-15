from django.contrib.auth.models import User
from rest_framework import serializers


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""

    password = serializers.CharField(
        max_length=32,
        min_length=4,
        write_only=True
    )

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'username', 'password']
        read_only_fields = ('id', )

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    """Serializers detail fields about user"""
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'username']
