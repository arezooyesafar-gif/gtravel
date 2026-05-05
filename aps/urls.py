import decimal
from django.contrib import admin
from django.http import HttpResponse
from order.views import submite_order, add_order_item, startPayment, remove_order_item, order_view, payWithWallet, \
    view_all_orders
from pages.views import page_detail
from payments.models import PaymentRequest
from theme.views import main_page_settings
from tour.utils import mypdf
from tour.views.views import PMemoriesCreate, memoriesSubmit
from . import settings
from django.conf.urls.static import static
from django.urls import path, include
from .ajax_views import *
from .sitemaps import StaticSitemap, blogSitemap, tourSitemap, hotelSitemap, tourContrySitemap, tourCitySitemap, \
    hotelCountrySitemap, hotelCitySitemap
from .views import *
from tour.views import *
from django.contrib.sitemaps.views import sitemap
from tour.models import *
from django.views.decorators.csrf import csrf_exempt
import requests
import json
from uuid import uuid4

sitemaps = {
    'static': StaticSitemap,
    'blog': blogSitemap,
    'tour': tourSitemap,
    'tourCountry': tourContrySitemap,
    'tourCity': tourCitySitemap,
    'hotel': hotelSitemap,
    'hotelCountry': hotelCountrySitemap,
    'hotelCity': hotelCitySitemap,
}

def read_robot(request):
    frb = open('robots.txt', 'r')
    file_content = frb.read()
    frb.close()
    return HttpResponse(file_content, content_type="text/plain")

def read_search(request):
    frb = open('google953f8aa654184902.html', 'r')
    file_content = frb.read()
    frb.close()
    return HttpResponse(file_content, content_type="text/html")


def payment(request):
    return render(request, 'payment.html')


@csrf_exempt
def get_token_for_payment(request):
    try:
        body = request.POST
        amount = int(body['amount'].replace(',', ''))
        res_number = str(uuid4().int)
        url = "https://sep.shaparak.ir/onlinepg/onlinepg"
        payload = json.dumps({
            "action": "token",
            "TerminalId": "15278676",
            "Amount": amount,
            "ResNum": res_number,
            "RedirectUrl": "https://arezoosafar.com/payment-redirect",
            "CellNumber": body['phoneNumber']
        })
        headers = {'Content-Type': 'application/json'}
        response = requests.request("POST", url, headers=headers, data=payload).json()
        if response['status'] == 1:
            PaymentRequest.objects.create(
                contract_number=body['contractNumber'],
                full_name=body['fullName'],
                phone_number=body['phoneNumber'],
                amount=decimal.Decimal(amount),
                description=body['description'],
                terminal_id="15278676",
                res_number=res_number,
                token=response['token'],
            )
        date = datetime.now()
        context = dict(
            token=response['token'],
            amount=body['amount'],
            phoneNumber=body['phoneNumber'],
            fullName=body['fullName'],
            contractNumber=body['contractNumber'],
            description=body['description'],
            createdAT=date
        )
        return render(request, 'confirm_payment.html', context=context)
    except TypeError:
        return render(request, 'payment.html')



@csrf_exempt
def payment_redirect(request):
    try:
        body = request.POST
        status = int(body['Status'])
        rrn = body.get('Rrn')
        ref_num = body.get('RefNum')
        res_num = body.get('ResNum')
        trace_num = body.get('TraceNo')
        amount = body.get('Amount')
        secure_pan = body.get('SecurePan')
        token = body.get('Token')
        hashed_card_number = body['HashedCardNumber']
        payment_request = PaymentRequest.objects.get(token=token)
        if payment_request.status == 2:
            return render(request, 'failed_payment.html')
        payment_request.rrn = rrn
        payment_request.ref_number = ref_num
        payment_request.trace_number = trace_num
        payment_request.secure_pan = secure_pan
        payment_request.secure_pan = secure_pan
        payment_request.hashed_card_number = hashed_card_number
        payment_request.callback_status_code = status
        payment_request.save()
        if status == 2:
            url = "https://sep.shaparak.ir/verifyTxnRandomSessionkey/ipg/VerifyTransaction"
            payload = json.dumps({
                "RefNum": ref_num,
                "TerminalNumber": 15278676
            })
            headers = {'Content-Type': 'application/json'}
            response = requests.request("POST", url, headers=headers, data=payload).json()
            now = datetime.now()
            context = dict(rrn=rrn, amount=amount, createdAT=now)
            if response['ResultCode'] == 0:
                payment_request.status = 2
                payment_request.verify_result_code = 0
                payment_request.save()
                return render(request, 'success_payment.html', context=context)
            payment_request.verify_result_code = response['ResultCode']
            payment_request.save()
            return render(request, 'failed_payment.html', context=context)
        else:
            return render(request, 'failed_payment.html')
    except:
        return render(request, 'failed_payment.html')


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('chaining/', include('smart_selects.urls')),
    path('dashboard/', include('tour.urls')),
    path('dashboard/blog/', include('blog.urls')),
    path('user/', include('person.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('captcha/', include('captcha.urls')),
    path('pages/', include('pages.urls')),
    path('dashboard/wallet/', include('wallet.urls')),
    path('dashboard/hotels/', include('hotels.urls')),
    path('dashboard/online-orders/', include('order.urls')),
    path('', (IndexPage), name='index-page'),
    path('visa/request', visa_request, name='visa_request'),
    path('visa/request/thai', thai_visa_request, name='thai_visa_request'),
    #tours urls
    path('all-tour', (AllTourList), name='all-tour'),
    path('<str:slug>/<int:id>/city-tours', CityTourList, name='city-tours'),
    path('<str:slug>/<int:id>/all-tour', (CategoryTourList), name='all-tour-country'),
    path('tour/<int:id>/<str:Slug>', TourDetail, name='tour-detail'),
    path('tour/<str:slug>', MenuTourList, name='MenuTourList'),

    #hotels urls
    path('all-hotel', (AllHotelList), name='all-hotel'),
    path('all-hotel/<int:id>/<str:slug>', (AllHotelCity), name='all-hotel-city-list'),
    path('all-country-hotel/<int:id>/<str:slug>', (AllCountryHotel), name='all-hotel-list'),
    path('hotels/<int:id>/<str:Slug>', (HotelDetail), name='hotel-detail'),
    path('<str:slug>/<int:id>/origin_tour_city', CityTourListOrigin, name='CityTourListOrigin'),
    path('norooz_tours', (AllTourList_norooz), name='norooz_tours'),
    path('installment_tours', (AllTourList_Installment), name='installment_tours'),
    path('<str:slug>/<int:id>/origin-tours', (all_tour_list_origins), name='all_tour_list_origins'),
    path('search-result', (TourSearch), name='search-result'),
    path('blog', (BlogPage), name='blog'),
    path('blog/<str:slug>/<int:id>', (CategoryPost), name='blog-category'),
    path('blog/<int:id>/<str:slug>', (PostDetail), name='post-detail'),
    path('russia_visa', russia_visa, name='russia_visa'),


    path('hotel_search', (hotel_search), name='hotel_search'),
    path('about-us', (AboutUsUi), name='about-us'),
    path('contact-us', (ContactUsUi), name='contact-us'),
    path('pages/<str:slug>', page_detail, name='page_detail'),
    path('ajax_dest', ajax_dest, name='ajax_dest'),
    path('pdf-download/<int:id>', mypdf, name='pdf-download'),
    path('dashboard/theme/main_page/<int:id>', (main_page_settings), name='main_page_settings'),
    path("sitemap.xml", sitemap,
         {"sitemaps": sitemaps},
         name="django.contrib.sitemaps.views.sitemap",
         ),
    path('robots.txt', read_robot),
    path('google953f8aa654184902.html', read_search),
    path('memories', (PMemoriesCreate), name='memories'),
    path('itineraries/<str:slug>', (CategoryMemo), name='memory-category'),
    path('read-jounery/<int:id>', (singleMemoView), name='read-jounery'),
    path('order-track', orderView, name='order-track'),
    path('order-view/<int:id>/<str:OrderCode>', singleOrderView, name='order-view'),
    path('search-order', OrderTrack, name='search-order'),
    path('order-info/<int:id>/<str:OrderCode>', orderInfo, name='order-info'),
    path('submit-memory/<int:id>', memoriesSubmit, name='submit-memo'),

    path('reserve/<int:tour_id>/<int:package_id>', submite_order, name='submite_order'),
    path('add_order_item', add_order_item, name='add_order_item'),
    path('remove_order_item/<int:id>', remove_order_item, name='remove_order_item'),
    path('view_all_orders/', view_all_orders, name='view_all_orders'),
    path('order_view/<int:id>', order_view, name='order_view'),
    path('startPayment/<int:id>', startPayment, name='startPayment'),
    path('payWithWallet/<int:id>', payWithWallet, name='payWithWallet'),
    path('country_tour_cities', get_country_tours_city, name='get_country_tours_city'),
    path('get_country_tours_city_canvas', get_country_tours_city_mobile, name='get_country_tours_city_mobile'),

    # ajax views

    path('toursdata', index_tours_ajax, name='index_tours_ajax'),
    path('tourslist', list_tours_ajax, name='list_tours_ajax'),
    path('tourslisth', list_tours_ajax_horzental, name='list_tours_ajax'),
    path('tourslistm', list_tours_ajax_menu_horzental, name='list_tours_ajax_menu_horzental'),
    path('country_tours_ajax', country_tours_ajax, name='country_tours_ajax'),
    path('city_tours_ajax', city_tours_ajax, name='city_tours_ajax'),
    path('postdata', index_posts_ajax, name='index_posts_ajax'),
    path('hotel_cities_ajax', (hotel_cities_ajax), name='hotel_cities_ajax'),
    path('country_hotels_ajax', country_hotels_ajax, name='country_hotels_ajax'),
    path('city_hotels_ajax', city_hotels_ajax, name='city_hotels_ajax'),
    path('get_country_city', get_country_city, name='get_country_city'),
    path('sidebar_filter', sidebar_filter, name='sidebar_filter'),
    path('sidebar_filter_city', sidebar_filter_city, name='sidebar_filter_city'),
    path('menuSearch', menuSearch, name='menuSearch'),
    path('add-reply', add_reply, name='add_reply'),
    path('submit-cm', submitCm, name='submitCm'),
    path('submit-hotel-cm', submitHotelCm, name='submitHotelCm'),
    path('payment', payment, name='payment'),
    path('get-token', get_token_for_payment, name='get_token_for_payment'),
    path('payment-redirect', payment_redirect, name='payment_redirect'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
handler404='aps.views.handler404'