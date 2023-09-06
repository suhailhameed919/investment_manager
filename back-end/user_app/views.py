from django.shortcuts import render
from django.contrib.auth import authenticate
from user_app.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from user_app.serializers import UserSerializer

# Create your views here.
class Sign_Up(APIView):
    def post(self, request):
        try:
            request.data["username"] = request.data["email"]
            newUser = User.objects.create_user(**request.data)
            print(newUser.email)
            print(newUser)

            token = Token.objects.create(user=newUser)
            return Response(
                {"user": newUser.email, "token": token.key}, status=HTTP_201_CREATED
            )
        
        except Exception as e: 
            
            return Response(
                {"message": "user already registered"}, 
                print(e),
                status = HTTP_400_BAD_REQUEST
            )
            

class Info(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    def get(self, request):
        return Response({"username": request.user.email})




class Log_in(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        currentUser = authenticate(username=email, password=password)
        if currentUser:
            token, created = Token.objects.get_or_create(user=currentUser)
            return Response({"token": token.key, "user": currentUser.email})
        else:
            return Response("user not matching credentials", status=HTTP_404_NOT_FOUND)

class Log_out(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=HTTP_204_NO_CONTENT)

