from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Transaction
from .serializers import Transaction_serializer
import requests


class TransactionListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        transaction = Transaction.objects.filter(user_id=request.user)
        serializer = Transaction_serializer(transaction, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    
    def post(self, request):
        transaction = Transaction.objects.create(
            account=request.data.get('account'),
            amount=request.data.get('amount'),
            category=request.data.get('category'),
  
            user_id=request.user
        )
        return Response(Transaction_serializer(transaction).data, status=HTTP_201_CREATED)
    
