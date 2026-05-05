from django.urls import path, include

from order.ajax_views import ajax_wallet_transaction
from .views import *

urlpatterns = [
    path('wallet_data/<int:id>', user_wallet, name='wallet_data'),
    path('ajax_wallet_withdrawal', ajax_wallet_withdrawal, name='ajax_wallet_withdrawal'),
    path('ajax_wallet_deposite', ajax_wallet_deposite, name='ajax_wallet_deposite'),
    path('start_wallet_charge', start_wallet_charge, name='start_wallet_charge'),
]