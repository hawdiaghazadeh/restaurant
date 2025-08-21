from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


from .serializers import ProfileSerializer, RegisterSerializer, LoginSerializer, \
    ChangePasswordSerializer


class RegisterView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, default='user@example.com'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, default='********'),
                'password2': openapi.Schema(type=openapi.TYPE_STRING, default='********'),
            },
            required=['email', 'password', 'password2']
        ),
        tags=['Authentication']
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()
        return Response(ProfileSerializer(user).data, status=status.HTTP_201_CREATED)



class LoginView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, default='user@example.com'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, default='********'),
            },
            required=['email', 'password']
        ),
        tags=['Authentication']
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        response = Response({'message': 'login success'})
        response.set_cookie(key='access_token', value=access_token, httponly=settings.COOKIE_HTTPONLY, samesite=settings.COOKIE_SAMESITE, secure=settings.COOKIE_SECRET)
        response.set_cookie(key='refresh_token', value=str(refresh), httponly=settings.COOKIE_HTTPONLY, samesite=settings.COOKIE_SAMESITE, secure=settings.COOKIE_SECRET)

        return response


class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'old_password': openapi.Schema(type=openapi.TYPE_STRING, default='********'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, default='********'),
                'password2': openapi.Schema(type=openapi.TYPE_STRING, default='********'),
            },
            required=['old_password', 'password', 'password2']
        ),
        tags=['Authentication']
    )
    def post(self, request):
        serializer = ChangePasswordSerializer(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Password changed'}, status=status.HTTP_200_OK)



class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Authentication']
    )
    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")
        if refresh_token:
            try:
                RefreshToken(refresh_token).blacklist()
            except Exception:
                pass
        response = Response({"message": "Logged out"})
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response
