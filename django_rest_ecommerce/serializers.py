from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Cart, Order, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "owner", "name", "description",
                  "image_url", "price", "stock"]

    def to_representation(self, instance):
        result = super().to_representation(instance)
        # Exclude the owner field so that we don't end up exposing who owns a product
        del result["owner"]
        return result


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ["id", "owner", "items"]

    def to_representation(self, instance):
        result = super().to_representation(instance)
        # Exclude the owner and the id fields because they're not really necessary
        del result["owner"]
        del result["id"]
        return result


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "owner", "items", "status"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class SignUpSerializer(LoginSerializer):
    email = serializers.EmailField()
