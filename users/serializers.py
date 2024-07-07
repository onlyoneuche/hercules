from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['userId', 'firstName', 'lastName', 'email', 'phone']
        extra_kwargs = {'password': {'write_only': True}}


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['firstName', 'lastName', 'email', 'password', 'phone']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError("Email already registered")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            firstName=validated_data['firstName'],
            lastName=validated_data['lastName'],
            email=validated_data['email'],
            password=validated_data['password'],
            phone=validated_data.get('phone', '')
        )
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        token['firstName'] = user.firstName
        token['lastName'] = user.lastName

        return token
