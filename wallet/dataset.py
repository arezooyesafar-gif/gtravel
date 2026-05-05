from .models import *

def get_withdrawal_transactions(wallet_id):
    withdrawal_recoreds = walletTransaction.objects.filter(wallet=wallet_id,withdrawal=True).order_by('-timestamp')
    return withdrawal_recoreds