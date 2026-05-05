from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from wallet.models import walletTransaction
from .models import *

def ajax_paid_order(request):
    paid_orders = order.objects.filter(paid=True)
    paginator = Paginator(paid_orders, 5)
    page = request.GET.get('page')
    paid_orders = paginator.get_page(page)
    context = {
        'orders': paid_orders
    }
    return render(request, 'order/ajax/order_list.html', context)

def all_ajax_paid_order(request):
    trs_code = request.GET.get('trs_code')
    paid_date = request.GET.get('paid_date')
    submit_date = request.GET.get('submit_date')
    paid_orders = order.objects.filter(paid=True)
    if trs_code:
        paid_orders = paid_orders.filter(order_number=trs_code)
    if submit_date:
        paid_orders = paid_orders.filter(order_date=submit_date)
    if paid_date:
        paid_orders = paid_orders.filter(paid_date=paid_date)
    paginator = Paginator(paid_orders, 10)
    page = request.GET.get('page')
    paid_orders = paginator.get_page(page)
    context = {
        'orders': paid_orders
    }
    return render(request, 'order/ajax/ajax_all_paid_orders.html', context)

def all_ajax_pending_order(request):
    trs_code = request.GET.get('trs_code')
    paid_date = request.GET.get('paid_date')
    submit_date = request.GET.get('submit_date')
    pending_orders = order.objects.filter(paid=False)
    if trs_code:
        paid_orders = pending_orders.filter(order_number=trs_code)
    if submit_date:
        paid_orders = pending_orders.filter(order_date=submit_date)
    if paid_date:
        paid_orders = pending_orders.filter(paid_date=paid_date)
    paginator = Paginator(pending_orders, 10)
    page = request.GET.get('page')
    paid_orders = paginator.get_page(page)
    context = {
        'orders': paid_orders
    }
    return render(request, 'order/ajax/ajax_all_pending_orders.html', context)

def ajax_pending_order(request):
    pending_orders = order.objects.filter(paid=False)
    paginator = Paginator(pending_orders, 5)
    page = request.GET.get('page')
    pending_orders = paginator.get_page(page)
    context = {
        'orders': pending_orders
    }
    return render(request, 'order/ajax/pending_order_list.html', context)

def ajax_wallet_transaction(request):
    all_records = walletTransaction.objects.all().order_by('-timestamp')
    paginator = Paginator(all_records, 10)
    page = request.GET.get('page')
    all_records = paginator.get_page(page)
    context = {
        'all_records': all_records
    }
    return render(request, 'order/ajax/wallet_transaction_list.html', context)