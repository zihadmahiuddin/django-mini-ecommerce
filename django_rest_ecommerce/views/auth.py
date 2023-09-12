from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.urls import path
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.views import token_refresh

from ..serializers import LoginSerializer, SignUpSerializer, UserSerializer


@api_view(["POST"])
def login(request: Request):
    data = request.data
    login_serializer = LoginSerializer(data=data)
    if login_serializer.is_valid():
        username = login_serializer.data["username"]
        password = login_serializer.data["password"]

        user = authenticate(username=username, password=password)

        if user is None:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
            )

        token = AccessToken.for_user(user)
        refresh_token = RefreshToken.for_user(user)

        return Response({
            "access_token": str(token),
            "refresh_token": str(refresh_token),
        })

    return Response(
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(["POST"])
def signup(request: Request):
    sign_up_serializer = SignUpSerializer(data=request.data)
    if sign_up_serializer.is_valid():
        user = User(username=sign_up_serializer.data["username"],
                    email=sign_up_serializer.data["email"], password=sign_up_serializer.data["password"])
        user.set_password(user.password)
        user.save()

        token = AccessToken.for_user(user)
        refresh_token = RefreshToken.for_user(user)

        user_serializer = UserSerializer(user)
        return Response({
            "access_token": str(token),
            "refresh_token": str(refresh_token),
            "user": user_serializer.data
        })

    return Response(sign_up_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


auth_view = (
    [
        path("login", login),
        path("signup", signup),
        path("token/refresh", token_refresh, name="token_refresh")
    ],
    "auth",
    "auth",
)
