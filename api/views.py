from django.shortcuts import render
from rest_framework.views import APIView
from api.serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny #@loginrequird in drf
from django.http import Http404

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


class PersonList(APIView):
    def get(self, request, format=None):
        person = Person.objects.all()
        serializer = PersonSerializer(person, many=True)
        return Response(serializer.data)
    
    
    
class PersonAdd(APIView):
    def get(self, request, format=None):
        person = Person.objects.all()
        serializer = PersonSerializer(person, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PersonId(APIView):
    def get_object(self, person_id):
        try:
            return Person.objects.get(id=person_id)
        except Person.DoesNotExist:
            raise Http404

    def get(self, request, person_id, format=None):
        person = self.get_object(person_id)
        serializer = PersonSerializer(person)
        return Response(serializer.data)

    def put(self, request, person_id, format=None):
        person = self.get_object(person_id)
        serializer = PersonSerializer(person, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, person_id, format=None):
        person = self.get_object(person_id)
        person.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)