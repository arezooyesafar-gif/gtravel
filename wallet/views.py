import datetime
import json
import requests
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from aps import settings
from person.models import person_profile
from .models import *
from .dataset import *

if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'
ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

def user_wallet(request, id):
    user = User.objects.get(id=id)
    user_wallet = wallet.objects.get(user_id=user.id)
    all_records = walletTransaction.objects.all()
    withdrawal_count = all_records.filter(withdrawal=True)
    deposit_count = all_records.filter(deposit=True)
    withdrawal_total = 0
    deposite_total = 0
    for i in withdrawal_count:
        withdrawal_total += i.amount
    for i in deposit_count:
        deposite_total += i.amount

    context = {
        'user_wallet': user_wallet,
        'withdrawal_count': withdrawal_count.count(),
        'withdrawal_total': withdrawal_total,
        'deposit_count': deposit_count.count(),
        'deposite_total': deposite_total
    }
    return render(request, 'wallet/user_wallet_info.html', context)

def ajax_wallet_withdrawal(request):
    wallet_id = request.GET.get('wallet_id')
    all_recoreds = walletTransaction.objects.filter(wallet_id=wallet_id, withdrawal=True).order_by('-id')
    paginator = Paginator(all_recoreds, 5)
    page = request.GET.get('page')
    all_recoreds = paginator.get_page(page)
    context = {
        'all_recoreds': all_recoreds
    }
    return render(request, 'ajax/wallet_withdrawal.html', context)

def ajax_wallet_deposite(request):
    wallet_id = request.GET.get('wallet_id')
    all_recoreds = walletTransaction.objects.filter(wallet_id=wallet_id, deposit=True).order_by('-id')
    paginator = Paginator(all_recoreds, 5)
    page = request.GET.get('page')
    all_recoreds = paginator.get_page(page)
    context = {
        'all_recoreds': all_recoreds
    }
    return render(request, 'ajax/wallet_deposit.html', context)

def charge_wallet(request):
    wallet_id = request.GET.get('wallet_id')
    amount = request.GET.get('amount')
    user_wallet = wallet.objects.get(id=wallet_id)
    user_wallet.balance += int(amount)
    user_wallet.save()
    new_transaction = walletTransaction.objects.create(wallet_id=wallet_id, amount=amount, deposit=True, timestamp=datetime.datetime.now())
    messages.success(request, "افزایش موجودی با موفقیت در سامانه ثبت گردید." )
    return redirect('wallet_data', request.user.id)

def start_wallet_charge(request):
    wallet_id = request.GET.get('wallet_id')
    amount = request.GET.get('amount')
    amount = int(amount)
    user_wallet = wallet.objects.get(id=wallet_id)
    user_profile = person_profile.objects.get(user=user_wallet.user.id)
    description = 'افزایش موجودی کیف پول'
    phone = user_profile.mobile_number
    new_transaction = walletTransaction.objects.create(wallet_id=wallet_id, amount=amount,
    deposit=True, timestamp=datetime.datetime.now())
    CallbackUrl = 'http://5.116.72.219/dashboard/wallet/varify_Charge' + str(new_transaction.id)
    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": amount,
        "Description": description,
        "Phone": phone,
        "CallbackURL": CallbackUrl,
    }
    data = json.dumps(data)
    headers = {'content-type': 'application/json', 'content-length': str(len(data))}
    response = requests.post(ZP_API_REQUEST, data=data, headers=headers)
    if response.status_code == 200:
        res = response.json()
        if res['Status'] == 100:
            return redirect(ZP_API_STARTPAY + res['Authority'])
    pass
