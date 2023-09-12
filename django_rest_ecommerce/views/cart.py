from django.urls import path
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication

from ..models import Cart
from ..serializers import CartSerializer


class CartView(CreateAPIView, RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Cart.objects.get(owner=user)
        return queryset

    def get(self, request: Request, *args, **kwargs):
        try:
            cart = self.get_queryset().get()
            return Response(self.serializer_class(cart).data)
        except Cart.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request: Request, *args, **kwargs):
        (cart, _) = Cart.objects.update_or_create(
            owner=request.user,
            defaults={
                "owner": request.user,
            }
        )
        cart.items.set(request.data["items"])
        return Response(self.serializer_class(cart).data)

    def put(self, request: Request, *args, **kwargs):
        (cart, _) = Cart.objects.update_or_create(
            owner=request.user,
            defaults={
                "owner": request.user,
            }
        )
        cart.items.set(request.data["items"])
        return Response(self.serializer_class(cart).data)

    def patch(self, request: Request, *args, **kwargs):
        (cart, _) = Cart.objects.update_or_create(
            owner=request.user,
            defaults={
                "owner": request.user,
            }
        )
        for item in request.data["items"]:
            cart.items.add(item)
        return Response(self.serializer_class(cart).data)

    def delete(self, request: Request, *args, **kwargs):
        try:
            cart = Cart.objects.get(owner=request.user)
        except Cart.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        self.kwargs["pk"] = cart.pk
        return self.destroy(request, *args, **kwargs)


cart_view = (
    [
        path("", CartView.as_view()),
    ],
    "cart",
    "cart",
)
