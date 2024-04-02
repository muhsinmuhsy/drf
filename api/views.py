from django.shortcuts import render
from rest_framework.views import APIView
from api.serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny #@loginrequird in drf
# Create your views here.

class RegisterAPI(APIView):
    def post(self,request):
        _data = request.data
        serializer = RegisterSerializer(data=_data)
        
        if not serializer.is_valid():
            return Response({'message': serializer.errors}, status=status.HTTP_404_NOT_FOUND)

        serializer.save()
        return Response({'message': 'User Created'}, status=status.HTTP_201_CREATED)


class LoginAPI(APIView):
    def post(self,request):
        _data = request.data
        serializer = LoginSerializer(data=_data)
        
        if not serializer.is_valid():
            return Response({'message':serializer.errors}, status=status.HTTP_404_NOT_FOUND)
        
        user = authenticate(username= serializer.data['username'], password= serializer.data['password'])
        
        if not user:
            return Response({'message':"Invalid"}, status=status.HTTP_404_NOT_FOUND)
        
        token, _ = Token.objects.get_or_create(user=user)
        
        return Response({'message' : 'Login Successfull', 'token': str(token)}, status=status.HTTP_200_OK)
    
# class CurrentUser(APIView):
#     def get(self, request):
#         try:
#             user = request.user
#             if user.is_authenticated:
#                 # Return information about the authenticated user
#                 return Response({'message': f'Authenticated as {user.username}'})
#             else:
#                 # Handle the case when the user is not authenticated
#                 return Response({'message': 'User is not authenticated'}, status=401)
#         except Exception as e:
#             # Handle any unexpected exceptions
#             return Response({'message': str(e)}, status=500)