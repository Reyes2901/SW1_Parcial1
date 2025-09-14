from django.shortcuts import render

from drf_yasg import openapi

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from .serializers import UsuarioSerializer, RegistroSerializer

# Registro de usuario
class RegistroAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    @swagger_auto_schema(request_body=RegistroSerializer)
    def post(self, request):
        serializer = RegistroSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "user": UsuarioSerializer(user).data,
                "token": Token.objects.get(user=user).key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login con token
class LoginAPIView(ObtainAuthToken):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        request_body=None,
        responses={200: openapi.Response("Sesión cerrada correctamente.")}
    )
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = response.data['token']
        user = Token.objects.get(key=token).user
        return Response({
            'token': token,
            'user': UsuarioSerializer(user).data
        })
#Logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class LogoutAPIView(APIView):
    def post(self, request):
        user = request.user
        if hasattr(user, 'auth_token'):
            user.auth_token.delete()
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)

# Perfil del usuario logueado
class PerfilAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    @swagger_auto_schema(
        responses={200: UsuarioSerializer()}
    )
    def get(self, request):
        serializer = UsuarioSerializer(request.user, context={'request': request})
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=UsuarioSerializer,
        responses={200: UsuarioSerializer()}
    )
    def put(self, request):
        serializer = UsuarioSerializer(
        request.user,
        data=request.data,
        partial=True,
        context={'request': request}  # <-- Esto es clave
    )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        