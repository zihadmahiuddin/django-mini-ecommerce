from django.urls import path
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication

from ..models import Product
from ..serializers import ProductSerializer


class IsOwnerReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.owner == request.user


class ProductListView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request: Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args, **kwargs):
        user = request.user
        if not user or not user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        request.data["owner"] = user.id
        return self.create(request, *args, **kwargs)


class ProductView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOwnerReadOnly]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request: Request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request: Request, *args, **kwargs):
        user = request.user
        if not user or not user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        request.data["owner"] = user.id

        return self.update(request, *args, **kwargs, owner=user)

    def patch(self, request: Request, *args, **kwargs):
        user = request.user
        if not user or not user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        return self.partial_update(request, *args, **kwargs)

    def delete(self, request: Request, *args, **kwargs):
        user = request.user
        if not user or not user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        return self.destroy(request, *args, **kwargs)


product_view = (
    [
        path("products", ProductListView.as_view()),
        path("product/<int:pk>", ProductView.as_view()),
    ],
    "products",
    "products",
)
