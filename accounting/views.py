from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout

from .serializers import RegisterSerializer, LoginSerializer


@api_view(['POST'])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({'message': 'Пользоваткль успешно зарегистирирован'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        login(request, user)
        return Response({'message': 'Вход выполнен'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response({'message': 'Выход выполне'}, status=status.HTTP_200_OK)
