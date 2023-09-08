from django.shortcuts import render
from django.http import JsonResponse
from investment_manager_env.api_keys import PLAID_CLIENT_ID, PLAID_SECRET
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
import plaid
from user_app.models import User

# Create your views here.
def create_link_token(request, user_id):
    # Initialize the Plaid client
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