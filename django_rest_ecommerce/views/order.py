from django.urls import path
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from ..models import Order
from ..serializers import OrderSerializer


class OrdersView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, *args, **kwargs):
        orders = Order.objects.filter(owner=request.user)
        return Response(OrderSerializer(orders, many=True).data)

    def post(self, request: Request, *args, **kwargs):
        request.data["owner"] = request.user.pk
        request.data["status"] = Order.Status.PENDING

        order_serializer = OrderSerializer(data=request.data)
        if not order_serializer.is_valid():
            return Response(data=order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        order_serializer.save()

        return Response(order_serializer.data)


class OrderView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, *args, **kwargs):
        try:
            order = Order.objects.get(pk=kwargs["pk"])

            # only allow viewing own orders for non staff users
            if order.owner != request.user and not order.owner.is_staff:
                # 404 in order to not expose the existence of a vaid order ID
                return Response(status=status.HTTP_404_NOT_FOUND)

            return Response(OrderSerializer(order).data)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request: Request, *args, **kwargs):
        try:
            order = Order.objects.get(pk=kwargs["pk"])

            # only allow deleting own orders for non staff users
            if order.owner != request.user and not order.owner.is_staff:
                # 404 in order to not expose the existence of a vaid order ID
                return Response(status=status.HTTP_404_NOT_FOUND)

            order.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


order_view = (
    [
        path("orders/", OrdersView.as_view()),
        path("order/<int:pk>", OrderView.as_view()),
    ],
    "order",
    "order",
)
