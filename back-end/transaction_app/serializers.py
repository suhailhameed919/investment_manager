from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from transaction_app.models import Transaction

class Transaction_serializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'account', 'amount', 'category']
        

