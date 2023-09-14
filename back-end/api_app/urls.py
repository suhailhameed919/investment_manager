from django.urls import path
from api_app.views import Create_link_Token

urlpatterns = [
    path('create_link_token/', Create_link_Token.as_view(), name='create_link_token'),
]

#     path('get_access_token/', get_access_token),
#     path('set_access_token/', set_access_token),
#     path('accounts/', accounts),
#     path('item/', item),
#     path('transactions/', transactions),
#     path('create_public_token/', create_public_token),
# ]

