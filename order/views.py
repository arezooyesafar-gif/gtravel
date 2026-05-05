import datetime
import json
import random
import requests
from django.shortcuts import render, redirect
import order.models
from wallet.models import *
from aps import settings
from pages.dataset import get_colm_two_pages, get_colm_tree_pages
from person.models import person_profile
from theme.models import index_page
from tour.dataset import *
from .forms import order_search_form
from .models import *

if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'
ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

def submite_order(request, tour_id, package_id):
    theme_setting = index_page.objects.get(id=1)
    reseller_menu = get_top_pages()
    footer_2 = get_colm_two_pages()
    footer_3 = get_colm_tree_pages()
    cities_menu = get_menu_cities()
    orgin_menu_cities = get_origin_menu_cities(69)
    person = request.user
    package = Package.objects.get(id=package_id)
    tour = Tour.objects.get(id=tour_id)
    user_order = order.objects.filter(user=person, order_close=False)
    order_items = []
    total_items_price = 0
    if user_order:
        order_items = orderItem.objects.filter(order=user_order[0])
        for i in order_items:
            total_items_price += i.total_item_price
    cities = TourCity.objects.filter(TourName_id=tour.id)
    context = {
        'package': package,
        'tour': tour,
        'reseller_menu': reseller_menu,
        'footer_2': footer_2,
        'footer_3': footer_3,
        'tours_cities_list': cities_menu,
        'orgin_menu_cities': orgin_menu_cities,
        'set': theme_setting,
        'cities': cities[0],
        'order_items': order_items,
        'total_items_price': total_items_price,
    }
    return render(request, 'order/submit_room.html', context)


def add_order_item(request):
    tour_id = request.GET.get('tour_id')
    package_id = request.GET.get('package_id')
    adult_count = int(request.GET.get('adult_count'))
    baby_wb_count = int(request.GET.get('baby_wb_count'))
    baby_wob_count = int(request.GET.get('baby_wob_count'))
    infont_count = int(request.GET.get('infont_count'))
    package = Package.objects.get(id=package_id)
    tour = Tour.objects.get(id=tour_id)
    user_order = order.objects.filter(order_close=False, user=request.user)
    if user_order:
        user_order = user_order[0]
        if adult_count == 3:
            total_item_price = package.DoubleBedPrice * adult_count
            new_order_item = orderItem.objects.create(order=user_order, package=package,
            tour=tour, adults=adult_count,adults_price=package.DoubleBedPrice, baby_with_bed=0,
            baby_with_out_bed=0, infont=0,
            total_item_price=total_item_price)
            user_order.order_total += total_item_price
            user_order.save()
            return redirect('submite_order', tour.id, package.id)
        if adult_count == 1:
            total_item_price = package.SingleBedPrice + (package.BabyWithBedPrice * baby_wb_count) + (
            package.BabyWithoutBedPrice * baby_wob_count) + (package.InfontPrice * infont_count)
            new_order_item = orderItem.objects.create(order=user_order, package=package,
            tour=tour, adults=adult_count, baby_with_bed=baby_wb_count,
            baby_with_out_bed=baby_wob_count,
            infont=infont_count, adults_price=package.SingleBedPrice, baby_with_bed_price = package.BabyWithBedPrice,
            baby_with_out_bed_price=package.BabyWithoutBedPrice,infont_price = package.InfontPrice,
            total_item_price=total_item_price)
            user_order.order_total += total_item_price
            user_order.save()
            return redirect('submite_order', tour.id, package.id)
        if adult_count == 2 :
            total_item_price = (package.DoubleBedPrice * adult_count) + (package.BabyWithBedPrice * baby_wb_count) + (
            package.BabyWithoutBedPrice * baby_wob_count) + (package.InfontPrice * infont_count)
            new_order_item = orderItem.objects.create(order=user_order, package=package,
            tour=tour, adults=adult_count, baby_with_bed=baby_wb_count,
            baby_with_out_bed=baby_wob_count, infont=infont_count, adults_price=package.DoubleBedPrice,
            baby_with_bed_price=package.BabyWithBedPrice,
            baby_with_out_bed_price=package.BabyWithoutBedPrice,
            infont_price=package.InfontPrice,
            total_item_price=total_item_price)
            user_order.order_total += total_item_price
            user_order.save()
            return redirect('submite_order', tour.id, package.id)
    else:
        order_number = random.randint(100000, 999999)
        user_order = order.objects.create(user=request.user, order_number=order_number)
        if adult_count == 3:
            total_item_price = package.DoubleBedPrice * adult_count
            new_order_item = orderItem.objects.create(order=user_order, package=package,
            tour=tour, adults=adult_count,adults_price=package.DoubleBedPrice, baby_with_bed=0,
            baby_with_out_bed=0, infont=0,
            total_item_price=total_item_price)
            user_order.order_total += total_item_price
            user_order.save()
            return redirect('submite_order', tour.id, package.id)
        if adult_count == 1:
            total_item_price = package.SingleBedPrice + (package.BabyWithBedPrice * baby_wb_count) + (
            package.BabyWithoutBedPrice * baby_wob_count) + (package.InfontPrice * infont_count)
            new_order_item = orderItem.objects.create(order=user_order, package=package,
            tour=tour, adults=adult_count, baby_with_bed=baby_wb_count,
            baby_with_out_bed=baby_wob_count,
            infont=infont_count, adults_price=package.SingleBedPrice, baby_with_bed_price = package.BabyWithBedPrice,
            baby_with_out_bed_price=package.BabyWithoutBedPrice,infont_price = package.InfontPrice,
            total_item_price=total_item_price)
            user_order.order_total += total_item_price
            user_order.save()
            return redirect('submite_order', tour.id, package.id)
        if adult_count == 2 :
            total_item_price = (package.DoubleBedPrice * adult_count) + (package.BabyWithBedPrice * baby_wb_count) + (
            package.BabyWithoutBedPrice * baby_wob_count) + (package.InfontPrice * infont_count)
            new_order_item = orderItem.objects.create(order=user_order, package=package,
            tour=tour, adults=adult_count, baby_with_bed=baby_wb_count,
            baby_with_out_bed=baby_wob_count, infont=infont_count, adults_price=package.DoubleBedPrice,
            baby_with_bed_price=package.BabyWithBedPrice,
            baby_with_out_bed_price=package.BabyWithoutBedPrice,
            infont_price=package.InfontPrice,
            total_item_price=total_item_price)
            user_order.order_total += total_item_price
            user_order.save()
            return redirect('submite_order', tour.id, package.id)
    return

def remove_order_item(request, id):
    order_item = orderItem.objects.get(id=id)
    package = order_item.package
    tour = order_item.tour
    user_order = order_item.order
    user_order.order_total -= order_item.total_item_price
    user_order.save()
    order_item.delete()
    return redirect('submite_order', tour.id,  package.id)

def view_all_orders(request):
    theme_setting = index_page.objects.get(id=1)
    reseller_menu = get_top_pages()
    footer_2 = get_colm_two_pages()
    footer_3 = get_colm_tree_pages()
    cities_menu = get_menu_cities()
    orgin_menu_cities = get_origin_menu_cities(69)
    all_orders = order.objects.filter(user=request.user)
    context = {
        'reseller_menu': reseller_menu,
        'footer_2': footer_2,
        'footer_3': footer_3,
        'tours_cities_list': cities_menu,
        'orgin_menu_cities': orgin_menu_cities,
        'set': theme_setting,
        'all_orders':all_orders
    }
    return render(request, 'order/order_list.html', context)

def order_view(request, id):
    theme_setting = index_page.objects.get(id=1)
    reseller_menu = get_top_pages()
    footer_2 = get_colm_two_pages()
    footer_3 = get_colm_tree_pages()
    cities_menu = get_menu_cities()
    orgin_menu_cities = get_origin_menu_cities(69)
    person = request.user
    user_wallet = wallet.objects.get(user=person)
    user_order = order.objects.get(id=id, user=person)
    order_items = orderItem.objects.filter(order=user_order)
    recoreds = walletTransaction.objects.filter(order=user_order, withdraw_form_order_payment=True, payment_stat=True)
    total_items_price = 0
    for i in order_items:
        total_items_price += i.total_item_price
    context = {
        'reseller_menu': reseller_menu,
        'footer_2': footer_2,
        'footer_3': footer_3,
        'tours_cities_list': cities_menu,
        'orgin_menu_cities': orgin_menu_cities,
        'set': theme_setting,
        'order_items': order_items,
        'total_items_price': total_items_price,
        'wallet': user_wallet,
        'recoreds':recoreds
    }
    return render(request, 'order/view_order.html', context)

def payWithWallet(request, id):
    user_wallet = wallet.objects.get(user=request.user)
    user_order = order.objects.get(id=id)
    if not user_wallet.balance == 0 and user_order.order_total > user_wallet.balance or user_order.order_total == user_wallet.balance:
        user_order.paid_amount = user_wallet.balance
        new_transaction = walletTransaction.objects.create(wallet=user_wallet,
        amount=user_wallet.balance,timestamp=datetime.datetime.now(),
        withdrawal=True, withdraw_form_order_payment=True,
        order=user_order, payment_stat=True,
        payment_refId=random.randint(100000, 999999))
        user_wallet.balance = 0
        if user_order.paid_amount == user_order.order_total:
            user_order.paid = True
            user_order.order_close = True
        user_order.save()
        user_wallet.save()
        return redirect('order_view', user_order.id)
    if user_order.order_total < user_wallet.balance:
        user_wallet.balance -= user_order.order_total
        user_order.paid_amount = user_order.order_total
        user_order.paid = True
        user_order.order_close = True
        new_transaction = walletTransaction.objects.create(wallet=user_wallet,
        amount=user_order.order_total, timestamp=datetime.datetime.now(),
        withdrawal=True, withdraw_form_order_payment=True, order=user_order,payment_stat=True,
        payment_refId=random.randint(100000,999999))
        user_order.save()
        user_wallet.save()
        return redirect('order_view', user_order.id)

def startPayment(request, id):
    user_order = order.objects.get(id=id)
    amount = user_order.debit()
    description = 'پرداخت رزرو تور'
    user_profile = person_profile.objects.get(user=user_order.user.id)
    phone = user_profile.mobile_number
    CallbackUrl = 'http://5.116.72.219/dashboard/wallet/varifyPayment' + str(user_order.id)
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

def online_order_dashboard(request):
    all_orders = order.objects.all()
    all_paid_order = all_orders.filter(order_close=True)
    all_pending_order = all_orders.filter(order_close=False)
    total_orders_price = 0
    total_paid_orders = 0
    total_pending_orders = 0
    for i in all_orders:
        total_orders_price += i.order_total
    for i in all_paid_order:
        total_paid_orders += i.order_total
    for i in all_pending_order:
        total_pending_orders += i.order_total
    context = {
        'total_orders_price': total_orders_price,
        'all_paid_order': all_paid_order.count(),
        'all_pending_order': all_pending_order.count(),
        'total_paid_orders': total_paid_orders,
        'total_pending_orders': total_pending_orders
    }
    return render(request, 'order/admin/dashboard.html', context)

def single_order(request, order_id):
    user_order = order.objects.get(id=order_id)
    user_order_items = orderItem.objects.filter(order_id=user_order.id)
    context = {
        'order': user_order,
        'order_items': user_order_items
    }
    return render(request, 'order/single_order.html', context)

def all_paid_orders(request):
    forms = order_search_form()
    context = {
        'forms': forms
    }
    return render(request, 'order/all_paid_order.html', context)

def all_pending_orders(request):
    forms = order_search_form()
    context = {
        'forms': forms
    }
    return render(request, 'order/all_paid_order.html', context)