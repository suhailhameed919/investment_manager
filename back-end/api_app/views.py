from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_201_CREATED,HTTP_401_UNAUTHORIZED
from rest_framework.response import Response
# Create your views here.

class Plaid_Api(APIView):
    def post(param1, param2):
        print("CREATE LINK TOKEN CALLING")
        return Response("CREATE LINK TOKEN CALLING")