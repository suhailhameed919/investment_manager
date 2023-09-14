from django.shortcuts import render
from django.http import JsonResponse
import plaid
from user_app.models import User
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR,HTTP_400_BAD_REQUEST
import json
from rest_framework.response import Response
from decouple import config
import base64
import os
import datetime as dt
import json
import time
from dotenv import load_dotenv
from plaid.model.payment_amount import PaymentAmount
from plaid.model.payment_amount_currency import PaymentAmountCurrency
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.recipient_bacs_nullable import RecipientBACSNullable
from plaid.model.payment_initiation_address import PaymentInitiationAddress
from plaid.model.payment_initiation_recipient_create_request import PaymentInitiationRecipientCreateRequest
from plaid.model.payment_initiation_payment_create_request import PaymentInitiationPaymentCreateRequest
from plaid.model.payment_initiation_payment_get_request import PaymentInitiationPaymentGetRequest
from plaid.model.link_token_create_request_payment_initiation import LinkTokenCreateRequestPaymentInitiation
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.asset_report_create_request import AssetReportCreateRequest
from plaid.model.asset_report_create_request_options import AssetReportCreateRequestOptions
from plaid.model.asset_report_user import AssetReportUser
from plaid.model.asset_report_get_request import AssetReportGetRequest
from plaid.model.asset_report_pdf_get_request import AssetReportPDFGetRequest
from plaid.model.auth_get_request import AuthGetRequest
from plaid.model.transactions_sync_request import TransactionsSyncRequest
from plaid.model.identity_get_request import IdentityGetRequest
from plaid.model.investments_transactions_get_request_options import InvestmentsTransactionsGetRequestOptions
from plaid.model.investments_transactions_get_request import InvestmentsTransactionsGetRequest
from plaid.model.accounts_balance_get_request import AccountsBalanceGetRequest
from plaid.model.accounts_get_request import AccountsGetRequest
from plaid.model.investments_holdings_get_request import InvestmentsHoldingsGetRequest
from plaid.model.item_get_request import ItemGetRequest
from plaid.model.institutions_get_by_id_request import InstitutionsGetByIdRequest
from plaid.model.transfer_authorization_create_request import TransferAuthorizationCreateRequest
from plaid.model.transfer_create_request import TransferCreateRequest
from plaid.model.transfer_get_request import TransferGetRequest
from plaid.model.transfer_network import TransferNetwork
from plaid.model.transfer_type import TransferType
from plaid.model.transfer_authorization_user_in_request import TransferAuthorizationUserInRequest
from plaid.model.ach_class import ACHClass
from plaid.model.transfer_create_idempotency_key import TransferCreateIdempotencyKey
from plaid.model.transfer_user_address_in_request import TransferUserAddressInRequest
from plaid.api import plaid_api


# Create your views here.   
class Create_link_Token(APIView):
     authentication_classes = [TokenAuthentication]
     permission_classes = [IsAuthenticated]
     def post(self, request):
        print(request.user.id)
        print(request.data)
        print(str(request.user))

        user_id = (str(request.user))
        PLAID_CLIENT_ID = config('PLAID_CLIENT_ID', default='', cast=str)
        
        PLAID_SECRET = config('PLAID_SECRET', default='', cast=str)
        
        # client = plaid.Client(
        #     client_id=PLAID_CLIENT_ID,
        #     secret=PLAID_SECRET,
        #     public_key=None,
        #     environment='sandbox',  # Change this to 'production' in a live environment
        # )

        # Create a Link token
        response = LinkTokenCreateRequestUser({
            'user': {
                'client_user_id': user_id,  # A unique identifier for the user
            },
            'client_name': 'investment_manager',
            'products': ['auth', 'transactions','balance'],
            'country_codes': ['US'],
            'language': 'en',
        })

        if response['status'] == 201:
            link_token = response['link_token']
            return JsonResponse({'link_token': link_token})
        else:
            return JsonResponse({'error': 'Link token generation failed'}, status=500)
        

class Set_Access_Token(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        public_token = request.data.get('public_token')
        client = plaid.Client(
            client_id=PLAID_CLIENT_ID,
            secret= PLAID_SECRET,
            environment='sandbox',  # Change this to 'production' in a live environment
        )

        try:
            exchange_request = plaid.ItemPublicTokenExchangeRequest(
                public_token=public_token)
            exchange_response = client.item_public_token_exchange(exchange_request)
            access_token = exchange_response['access_token']
            item_id = exchange_response['item_id']
            if 'transfer' in PLAID_PRODUCTS:
                transfer_id = authorize_and_create_transfer(access_token)
            return Response(exchange_response.to_dict(), status=HTTP_200_OK)
        except plaid.ApiException as e:
            return Response(json.loads(e.body), status=HTTP_400_BAD_REQUEST)
