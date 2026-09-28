"""
فید JSON خصوصی برای همگام‌سازی خودکار قیمت و اطلاعات تورها با سایت آژانس‌های همکار.
این endpoint فقط خواندنی است و همیشه از دیتابیس زنده خونده می‌شه، بنابراین هر تغییری
که در پنل مدیریت روی قیمت/تاریخ تور ثبت بشه، بلافاصله در خروجی این فید هم دیده می‌شه.
دسترسی فقط با کلید API معتبر (مدل ApiPartner، قابل مدیریت از /admin/) امکان‌پذیره.
"""
import json
import random
import string
from datetime import date as _date
from functools import wraps

from django.http import JsonResponse, Http404
from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt

from tour.dataset import roll_over_expired_tour_dates
from tour.models import ApiPartner, Tour, Package, TourCity, date_plan, TripPlan, tour_images, TourOrder
from tour.date_pricing import compute_tour_min_price, packages_for_date


def require_api_key(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        key = request.headers.get('X-API-Key') or request.GET.get('api_key')
        if not key:
            return JsonResponse(
                {'error': 'کلید API ارسال نشده است. هدر X-API-Key را ارسال کنید.'},
                status=401, json_dumps_params={'ensure_ascii': False},
            )
        try:
            partner = ApiPartner.objects.get(api_key=key, is_active=True)
        except ApiPartner.DoesNotExist:
            return JsonResponse(
                {'error': 'کلید API نامعتبر یا غیرفعال است.'},
                status=403, json_dumps_params={'ensure_ascii': False},
            )
        ApiPartner.objects.filter(pk=partner.pk).update(last_used_at=timezone.now())
        request.api_partner = partner
        return view_func(request, *args, **kwargs)
    return wrapper


def _abs_url(request, url):
    if not url:
        return None
    return request.build_absolute_uri(url)


def _hotel_entry(request, hotel, view, service, sold_out=False):
    if not hotel:
        return None
    entry = {
        'name': hotel.HotelName,
        'name_en': hotel.HotelNameEnglish,
        'rating': hotel.HotelRating,
        'view': view or None,
        'service': service or None,
        'address': hotel.HotelAddress or None,
        'sold_out': bool(sold_out),
    }
    if hotel.Slug:
        entry['url'] = _abs_url(request, reverse('hotel-detail', args=[hotel.id, hotel.Slug]))
    if hotel.HotelImage:
        entry['image'] = _abs_url(request, hotel.HotelImage.url)
    return entry


def _serialize_package(pkg, request):
    hotels = [
        _hotel_entry(request, pkg.HotelName, pkg.view_hotel, pkg.service_hotel,
                     pkg.hotel_sold_out),
        _hotel_entry(request, pkg.Mhotel, pkg.view_mhotel, pkg.service_mhotel,
                     pkg.mhotel_sold_out),
        _hotel_entry(request, pkg.M1hotel, pkg.view_m1hotel, pkg.service_m1hotel,
                     pkg.m1hotel_sold_out),
        _hotel_entry(request, pkg.M2hotel, pkg.view_m2hotel, pkg.service_m2hotel,
                     pkg.m2hotel_sold_out),
        _hotel_entry(request, pkg.M3hotel, pkg.view_m3hotel, pkg.service_m3hotel,
                     pkg.m3hotel_sold_out),
        _hotel_entry(request, pkg.M4hotel, pkg.view_m4hotel, pkg.service_m4hotel),
    ]
    return {
        'id': pkg.id,
        'available': not pkg.is_sold_out,
        'exclusive_to_departure': pkg.exclusive_date_plan.start_date.isoformat()
        if pkg.exclusive_date_plan_id and pkg.exclusive_date_plan.start_date else None,
        'hotels': [h for h in hotels if h],
        'price': {
            'currency': str(pkg.Pcry) if pkg.Pcry else None,
            'double_bed': pkg.DoubleBedPrice,
            'single_bed': pkg.SingleBedPrice,
            'child_with_bed': pkg.BabyWithBedPrice,
            'child_without_bed': pkg.BabyWithoutBedPrice,
            'infant': pkg.InfontPrice,
        },
        'price_foreign': {
            'currency': str(pkg.fr_Pcry) if pkg.fr_Pcry else None,
            'double_bed': pkg.DoubleBedPrice_doller,
            'single_bed': pkg.SingleBedPrice_doller,
            'child_with_bed': pkg.BabyWithBedPrice_doller,
            'child_without_bed': pkg.BabyWithoutBedPrice_doller,
            'infant': pkg.InfontPrice_doller,
        },
    }


def _serialize_flight(tc):
    return {
        'airline': tc.Airline.AirLineTitle if tc.Airline else None,
        'from_airport': tc.FromAirport.AirportFa if tc.FromAirport else None,
        'to_airport': tc.ToAirport.AirportFa if tc.ToAirport else None,
        'flight_time': tc.FlightTime,
        'flight_duration': tc.FlightDuration,
        'flight_class': tc.FlightClass,
        'is_return_flight': tc.flight_return,
        'is_inbound_flight': tc.flight_inbound,
        'transfer_group': tc.GTransfer,
        'transfer_vip': tc.QTransfer,
        'transfer_private': tc.STransfer,
    }


def _serialize_trip_plan(tp, request):
    return {
        'title': tp.title,
        'location': tp.location,
        'views': tp.views,
        'services': tp.services,
        'description': strip_tags(tp.description) if tp.description else None,
        'image': _abs_url(request, tp.plan_image.url) if tp.plan_image else None,
    }


def _base_price(all_packages, base_dp=None):
    """ارزون‌ترین قیمت مؤثر تور برای تاریخ پیش‌فرضش (با اعمال قیمت‌های دستیِ همون تاریخ)."""
    best = compute_tour_min_price(all_packages, base_dp)
    if not best:
        return 0, 0, 'تومان', 'دلار'
    return int(best['price'] or 0), int(best['price_dollar'] or 0), best['currency'], best['currency_foreign']


def _departures(tour, all_packages, base_price, base_price_dollar, currency,
                currency_foreign, request=None, base_dp=None):
    """تاریخ‌های برگزاری تور.

    هر تاریخ پکیج‌های مؤثر خودش را هم دارد: هتلی که فقط برای همان تاریخ اضافه
    شده، هتل جایگزین‌شده، ویو/سرویس بازنویسی‌شده، و «تکمیل ظرفیت» هر هتل در
    همان تاریخ. پکیج‌هایی که برای یک تاریخ حذف شده‌اند در آن تاریخ نمی‌آیند.
    """
    departures = []

    def entry(start, end, price, price_dollar, dp):
        row = {
            'start_date': start,
            'end_date': end,
            'price': price,
            'price_foreign': price_dollar,
            'currency': currency,
            'currency_foreign': currency_foreign,
        }
        if request is not None:
            row['packages'] = [
                _serialize_package(p, request) for p in packages_for_date(tour, dp)
            ]
        return row

    if tour.StartDate:
        departures.append(entry(
            tour.StartDate.isoformat(),
            tour.EndDate.isoformat() if tour.EndDate else None,
            base_price, base_price_dollar, base_dp,
        ))
    for dp in date_plan.objects.filter(tour=tour).exclude(start_date=tour.StartDate).order_by('start_date'):
        best = compute_tour_min_price(all_packages, dp)
        price = int(best['price'] or 0) if best else base_price
        price_dollar = int(best['price_dollar'] or 0) if best else base_price_dollar
        departures.append(entry(
            dp.start_date.isoformat() if dp.start_date else None,
            dp.end_date.isoformat() if dp.end_date else None,
            price, price_dollar, dp,
        ))
    return departures


def _serialize_tour(tour, request):
    all_packages = list(Package.objects.filter(TourName=tour).select_related(
        'HotelName', 'Mhotel', 'M1hotel', 'M2hotel', 'M3hotel', 'M4hotel', 'Pcry', 'fr_Pcry',
        'exclusive_date_plan'
    ).order_by('DoubleBedPrice', 'DoubleBedPrice_doller'))
    base_dp = date_plan.objects.filter(tour=tour, start_date=tour.StartDate).first()
    packages_qs = packages_for_date(tour, base_dp)
    base_price, base_price_dollar, currency, currency_foreign = _base_price(all_packages, base_dp)
    gallery = tour_images.objects.filter(tour=tour)

    return {
        'id': tour.id,
        'slug': tour.Slug,
        'title': tour.Title,
        'url': _abs_url(request, tour.get_absolute_url()),
        'country': tour.Tcountry.TitleC if tour.Tcountry else None,
        'destination_city': tour.Tcity.Name if tour.Tcity else None,
        'origin_city': tour.origin_city.Name if tour.origin_city else None,
        'night_count': tour.NightCount,
        'day_count': tour.DayCount,
        'is_installment': tour.Installment,
        'is_cash_only': tour.Cash,
        'is_published': tour.PubTour,
        'image': _abs_url(request, tour.TourImage.url) if tour.TourImage else None,
        'gallery': [_abs_url(request, g.image.url) for g in gallery if g.image],
        'short_description': strip_tags(tour.ShortDsc) if tour.ShortDsc else None,
        'description': strip_tags(tour.Description) if tour.Description else None,
        'cancel_policy': strip_tags(tour.cancel_policy) if tour.cancel_policy else None,
        'price': {
            'amount': base_price,
            'currency': currency,
            'amount_foreign': base_price_dollar,
            'currency_foreign': currency_foreign,
        },
        'departures': _departures(tour, all_packages, base_price, base_price_dollar,
                                  currency, currency_foreign, request, base_dp),
        'packages': [_serialize_package(p, request) for p in packages_qs],
        'flights': [_serialize_flight(tc) for tc in TourCity.objects.filter(TourName=tour).select_related('Airline', 'FromAirport', 'ToAirport')],
        'itinerary': [_serialize_trip_plan(tp, request) for tp in TripPlan.objects.filter(tour=tour).order_by('id')],
        'updated_at': tour.updateDate.isoformat() if tour.updateDate else None,
    }


@require_api_key
def tour_feed_detail(request, slug):
    try:
        tour = Tour.objects.select_related('Tcountry', 'Tcity', 'origin_city').get(Slug=slug, PubTour=True)
    except Tour.DoesNotExist:
        raise Http404
    if tour.StartDate and tour.StartDate <= _date.today():
        roll_over_expired_tour_dates(Tour.objects.filter(id=tour.id))
        tour.refresh_from_db()
    data = _serialize_tour(tour, request)
    return JsonResponse(data, json_dumps_params={'ensure_ascii': False}, content_type='application/json; charset=utf-8')


@require_api_key
def tour_feed_list(request):
    qs = Tour.objects.filter(PubTour=True).select_related('Tcountry', 'Tcity', 'origin_city').order_by('-id')
    country_slug = request.GET.get('country')
    city_slug = request.GET.get('city')
    if country_slug:
        qs = qs.filter(Tcountry__slug=country_slug)
    if city_slug:
        qs = qs.filter(Tcity__slug=city_slug)
    roll_over_expired_tour_dates(qs.filter(StartDate__lte=_date.today()))
    data = [_serialize_tour(t, request) for t in qs]
    return JsonResponse(
        {'count': len(data), 'results': data},
        json_dumps_params={'ensure_ascii': False},
        content_type='application/json; charset=utf-8',
    )


def _reserve_json_response(payload, status):
    return JsonResponse(payload, status=status, json_dumps_params={'ensure_ascii': False}, content_type='application/json; charset=utf-8')


def _int_or_default(value, default=0):
    try:
        n = int(value)
        return n if n >= 0 else default
    except (TypeError, ValueError):
        return default


@csrf_exempt
@require_api_key
def tour_reserve(request):
    """ثبت درخواست رزرو از طرف آژانس همکار؛ دقیقاً همون کاری که فرم رزرو خود سایت انجام می‌ده -
    یعنی فقط یه درخواست (لید) تو لیست سفارش‌های داشبورد ثبت می‌شه، نه پرداخت آنلاین یا تایید خودکار.
    مدیر سایت مثل بقیه‌ی سفارش‌ها پیگیریش می‌کنه؛ فقط تو لیست مشخصه از کدوم آژانس اومده.
    عمداً اسلاگ تور تو آدرس نیست - همون package_id (که از فید GET می‌گیرن) کافیه و خودش تور رو پیدا می‌کنه،
    که آژانس مجبور نباشه برای هر رزرو جدا اسلاگ تور رو هم بفرسته."""
    if request.method != 'POST':
        return _reserve_json_response({'error': 'فقط متود POST مجاز است.'}, 405)

    if request.content_type == 'application/json':
        try:
            payload = json.loads(request.body.decode('utf-8') or '{}')
        except (ValueError, UnicodeDecodeError):
            return _reserve_json_response({'error': 'بدنه‌ی درخواست JSON معتبر نیست.'}, 400)
    else:
        payload = request.POST

    package_id = payload.get('package_id')
    name = str(payload.get('name') or '').strip()
    family = str(payload.get('family') or '').strip()
    mobile = str(payload.get('mobile') or '').strip()

    errors = {}
    package = None
    if not package_id:
        errors['package_id'] = 'شناسه‌ی پکیج (package_id) الزامی است.'
    else:
        try:
            package = Package.objects.select_related('TourName').get(id=package_id, TourName__PubTour=True)
        except (Package.DoesNotExist, ValueError, TypeError):
            errors['package_id'] = 'پکیجی با این شناسه پیدا نشد.'
        else:
            if package.is_sold_out:
                errors['package_id'] = 'این پکیج پر شده و دیگر قابل رزرو نیست.'
    if not name:
        errors['name'] = 'نام (name) الزامی است.'
    if not family:
        errors['family'] = 'نام خانوادگی (family) الزامی است.'
    if not mobile:
        errors['mobile'] = 'شماره موبایل (mobile) الزامی است.'

    if errors:
        return _reserve_json_response({'success': False, 'errors': errors}, 400)

    order_code = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))
    order = TourOrder.objects.create(
        OrderTour=package.TourName,
        Orderpackage=package,
        OrderTime=timezone.now(),
        OrderCode=order_code,
        OrderPack=str(package.id),
        Name=name,
        Family=family,
        Mobile=mobile,
        adult=_int_or_default(payload.get('adult'), 1),
        adult2=_int_or_default(payload.get('adult_single')),
        chield=_int_or_default(payload.get('child_with_bed')),
        chield2=_int_or_default(payload.get('child_without_bed')),
        infont=_int_or_default(payload.get('infant')),
        description=str(payload.get('description') or '')[:1000],
        api_partner=request.api_partner,
    )
    return _reserve_json_response({
        'success': True,
        'order_id': order.id,
        'order_code': order.OrderCode,
        'status': order.OrderStat,
        'message': 'درخواست رزرو با موفقیت ثبت شد؛ همکاران ما به‌زودی پیگیری می‌کنند.',
    }, 201)
