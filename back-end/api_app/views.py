from django.shortcuts import render
from django.http import JsonResponse
from investment_manager_env.api_keys import PLAID_CLIENT_ID, PLAID_SECRET, PLAID_PRODUCTS, PLAID_ENV, PLAID_COUNTRY_CODES,PLAID_REDIRECT_URI
import plaid
from user_app.models import User
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR,HTTP_400_BAD_REQUEST

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
    def post(self, request):
        public_token = request.data.get('public_token')

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