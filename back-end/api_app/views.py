from django.shortcuts import render
from django.http import JsonResponse
from investment_manager_env.api_keys import PLAID_CLIENT_ID, PLAID_SECRET, PLAID_PRODUCTS, PLAID_ENV, PLAID_COUNTRY_CODES,PLAID_REDIRECT_URI
import plaid
from user_app.models import User
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR,HTTP_400_BAD_REQUEST
import json
from rest_framework.response import Response
# Create your views here.
class Create_link_Token(APIView):
     authentication_classes = [TokenAuthentication]
     permission_classes = [IsAuthenticated]
     def post(request):
        # Initialize the Plaid client
        user_id = request.user.id
        client = plaid.Client(
            client_id=PLAID_CLIENT_ID,
            secret= PLAID_SECRET,
            environment='sandbox',  # Change this to 'production' in a live environment
        )

        # Create a Link token
        response = client.LinkToken.create({
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
        



        # This is a helper function to authorize and create a Transfer after successful
        # exchange of a public_token for an access_token. The transfer_id is then used
        # to obtain the data about that particular Transfer.
        # def authorize_and_create_transfer(access_token):
        #     try:
        #         # We call /accounts/get to obtain first account_id - in production,
        #         # account_id's should be persisted in a data store and retrieved
        #         # from there.
        #         request = AccountsGetRequest(access_token=access_token)
        #         response = client.accounts_get(request)
        #         account_id = response['accounts'][0]['account_id']

        #         request = TransferAuthorizationCreateRequest(
        #             access_token=access_token,
        #             account_id=account_id,
        #             type=TransferType('credit'),
        #             network=TransferNetwork('ach'),
        #             amount='1.34',
        #             ach_class=ACHClass('ppd'),
        #             user=TransferAuthorizationUserInRequest(
        #                 legal_name='FirstName LastName',
        #                 email_address='foobar@email.com',
        #                 address=TransferUserAddressInRequest(
        #                     street='123 Main St.',
        #                     city='San Francisco',
        #1                     region='CA',
        #                     postal_code='94053',
        #                     country='US'
        #                 ),
        #             ),
        #         )
        #         response = client.transfer_authorization_create(request)
        #         pretty_print_response(response)
        #         authorization_id = response['authorization']['id']

        #         request = TransferCreateRequest(
        #             access_token=access_token,
        #             account_id=account_id,
        #             authorization_id=authorization_id,
        #             description='Payment')
        #         response = client.transfer_create(request)
        #         pretty_print_response(response)
        #         return response['transfer']['id']
        #     except plaid.ApiException as e:
        #         error_response = format_error(e)
        #         return jsonify(error_response)