from datetime import date as _date
from operator import attrgetter
from django.core.paginator import Paginator
from django.db.models import Count
from blog.models import blogPosts, PostCategory
from hotels.models import Hotel_Data
from .models import *
from tour.date_pricing import tour_card_packages, tour_card_packages_bulk
from pages.models import *
from django.core.cache import cache

def get_all_country():
    return Country.objects.all()

def get_all_city():
    return City.objects.all()
def get_airline_list():
    return AirLineData.objects.all().order_by('-id')
def get_top_pages():
    return pages.objects.filter(reseller=True, publish=True)

def get_all_tours():
    return Tour.objects.all().order_by('-id')

def get_all_pub_tours():
    pub_tours = Tour.objects.filter(PubTour=True).select_related('Tcountry', 'Tcity', 'origin_city').order_by('-updateDate')
    return pub_tours

def get_all_pub_tours_dates():
    dates = date_plan.objects.all()
    return dates

def roll_over_expired_tour_dates(tours):
    today = _date.today()
    for tour in tours:
        if tour.force_pub:
            continue
        next_plan = date_plan.objects.filter(tour=tour, start_date__gt=today).order_by('start_date').first()
        if next_plan:
            tour.StartDate = next_plan.start_date
            tour.EndDate = next_plan.end_date
            tour.save(update_fields=['StartDate', 'EndDate'])
        else:
            tour.PubTour = False
            tour.save(update_fields=['PubTour'])
        date_plan.objects.filter(tour=tour, start_date__lte=today).delete()

def get_all_pub_tours_admin():
    return Tour.objects.filter(PubTour=True).order_by('-id')

def get_all_unpub_tours():
    return get_all_tours().filter(PubTour=False).order_by('-id')

def get_all_city_media(city_id):
    return CityCountryMedia.objects.filter(city_id=city_id)

def get_all_country_media(country_id):
    return CityCountryMedia.objects.filter(country_id=country_id)

def get_all_country_faq(contry_id):
    return FAQ.objects.filter(Countryfaq=contry_id)

def get_all_city_faq(city_id):
    return cityFAQ.objects.filter(Cityfaq=city_id)

def get_all_tour_cat_faq(category_id):
    return TourCategoryFAQ.objects.filter(category=category_id)

def tour_cities_bulk(tours):
    """{tour_id: [TourCity...]} با یک کوئری، به‌جای یک کوئری به ازای هر تور."""
    tours = [t for t in tours if t]
    if not tours:
        return {}
    by_tour = {}
    qs = list(TourCity.objects.filter(
        TourName_id__in=[t.id for t in tours]
    ).select_related('Airline', 'FromAirport', 'ToAirport'))
    for c in qs:
        by_tour.setdefault(c.TourName_id, []).append(c)
    return by_tour


def get_all_tours_cities_data():
    tours = list(get_all_tours())
    bulk = tour_cities_bulk(tours)
    return [bulk.get(t.id, []) for t in tours]

def get_tours_cities_data():
    tours = list(get_all_pub_tours())
    bulk = tour_cities_bulk(tours)
    return [bulk.get(t.id, []) for t in tours]

def get_tours_packages_data():
    tours = list(get_all_pub_tours())
    bulk = tour_card_packages_bulk(tours)
    return [([bulk.get(t.id)[0]] if bulk.get(t.id) else []) for t in tours]

def get_spacial_tours():
    spacial_tours = Tour.objects.filter(Feature=True, PubTour=True).only('Title', 'NightCount', 'TourImage')
    _bulk = tour_card_packages_bulk(list(spacial_tours))
    spacial_packages = [_bulk.get(t.id, []) for t in spacial_tours]
    _cbulk = tour_cities_bulk(list(spacial_tours))
    spacial_cities = [_cbulk.get(t.id, []) for t in spacial_tours]
    spacialData = zip(spacial_tours, spacial_cities, spacial_packages)
    return spacialData

def get_all_pub_posts():
    return blogPosts.objects.filter(Publish=True).select_related('Category__parentCat').only('Title', 'slug', 'Image', 'Category').order_by('-id')

def get_menu_cities():
    tours_cities_name = sorted(set(Tour.objects.filter(PubTour=True, Tcity__isnull=False).values_list('Tcity__Name', flat=True)))
    slugs = {}
    for name, slug in City.objects.filter(Name__in=tours_cities_name).order_by('-id').values_list('Name', 'slug'):
        slugs[name] = slug
    tours_cities_slug = [slugs[name] for name in tours_cities_name]
    menu_cities = zip(tours_cities_name, tours_cities_slug)
    return menu_cities

def get_origins():
    origin_cities = []
    origin_tours = []
    for i in get_all_pub_tours():
        origin_cities.append(i.origin_city)
    origin_cities = list(set(origin_cities))
    for i in origin_cities:
        tour_num = Tour.objects.filter(origin_city=i, PubTour=True).count()
        if tour_num:
            origin_tours.append(tour_num)
    origins = zip(origin_cities, origin_tours)
    return origins

def get_tours_country():
    # قبلا به ازای هر تور یک کوئری برای کشور و یک کوئری برای شمارش می‌خورد
    counts = (
        Tour.objects.filter(PubTour=True, Tcountry__isnull=False)
        .values('Tcountry')
        .annotate(n=Count('id'))
    )
    by_id = {row['Tcountry']: row['n'] for row in counts}
    countries = list(Country.objects.filter(id__in=by_id.keys()))
    countries_tours = [by_id[c.id] for c in countries]
    return zip(countries, countries_tours)

def get_tours_cities():
    cities = []
    for i in Tour.objects.filter(PubTour=True).select_related('Tcity').order_by('-id'):
        cities.append(i.Tcity)
    cities = list(set(cities))
    return cities

def get_airlines():
    airlines = AirLineData.objects.all()
    return airlines

def get_tours_country_list():
    countries = Country.objects.filter(tocountry__PubTour=True).order_by('menu_order').distinct()
    return countries

# def get_country_tours(country_id):
#     tour_list = []
#     tours_query = related_tour_city.objects.filter(country=country_id, tour__PubTour=True)
#     tours_query = list(set(tours_query))
#     for i in tours_query:
#         tour_list.append(i.tour)
#     tour_list = list(set(tour_list))
#     tour_list = sorted(tour_list, key=attrgetter('updateDate'))
#     return tour_list
def get_country_tours(country_id):
    tour_list = []
    direct_tours = Tour.objects.filter(
        Tcountry_id=country_id,
        PubTour=True
    ).select_related('Tcountry', 'Tcity', 'origin_city')

    for tour in direct_tours:
        tour_list.append(tour)
    related_tours = related_tour_city.objects.filter(
        country_id=country_id,
        tour__PubTour=True
    ).select_related('tour', 'tour__Tcountry', 'tour__Tcity', 'tour__origin_city')

    for item in related_tours:
        tour_list.append(item.tour)
    unique_tours = {}
    for tour in tour_list:
        unique_tours[tour.id] = tour
    tour_list = sorted(
        unique_tours.values(),
        key=attrgetter('updateDate'),
        reverse=True
    )
    return tour_list

# def get_city_tours(city_id):
#     tour_list = []
#     tours_query = related_tour_city.objects.filter(city=city_id, tour__PubTour=True)
#     tours_query = list(set(tours_query))
#     for i in tours_query:
#         tour_list.append(i.tour)
#     tour_list = list(set(tour_list))
#     tour_list = sorted(tour_list, key=attrgetter('updateDate'))
#     return tour_list

def get_city_tours(city_id):
    tour_list = []
    direct_tours = Tour.objects.filter(
        Tcity_id=city_id,
        PubTour=True
    )
    for tour in direct_tours:
        tour_list.append(tour)
    related_tours = related_tour_city.objects.filter(
        city_id=city_id,
        tour__PubTour=True
    ).select_related('tour')
    for item in related_tours:
        tour_list.append(item.tour)
    unique_tours = {}
    for tour in tour_list:
        unique_tours[tour.id] = tour
    tour_list = sorted(
        unique_tours.values(),
        key=attrgetter('updateDate'),
        reverse=True
    )
    return tour_list

def get_city_tours_cities(city_id):
    tours = list(get_city_tours(city_id))
    bulk = tour_cities_bulk(tours)
    return [bulk.get(t.id, []) for t in tours]

def get_city_tours_packages(city_id):
    tours = list(get_city_tours(city_id))
    bulk = tour_card_packages_bulk(tours)
    return [bulk.get(t.id, []) for t in tours]

def get_country_tours_cities(country_id):
    tours = list(get_country_tours(country_id))
    bulk = tour_cities_bulk(tours)
    return [bulk.get(t.id, []) for t in tours]

def get_country_tours_packages(country_id):
    tours = list(get_country_tours(country_id))
    bulk = tour_card_packages_bulk(tours)
    return [bulk.get(t.id, []) for t in tours]

def get_country_tours_datePlan(country_id):
    datePlan = []
    tours = get_country_tours(country_id)
    for i in tours:
        datePlan.append(date_plan.objects.filter(tour=i).count())
    return datePlan

def get_contry_cities(country_id):
    """شهرهای یک کشور که صفحهٔ شهرشان واقعاً تور دارد، همراه با تعداد تور.

    قبلاً فقط شهرهایی برمی‌گشتند که «شهر اصلی» (Tcity) یک تور منتشرشده بودند و
    تطبیق هم با نام شهر انجام می‌شد. نتیجه این بود که مسکو و سن پترزبورگ در بخش
    مقصدهای صفحهٔ تور روسیه لینک نمی‌گرفتند، در حالی که صفحهٔ خودشان تور داشت —
    چون صفحهٔ شهر علاوه بر Tcity، شهرهای مرتبط (related_tour_city) را هم حساب
    می‌کند. حالا همان قاعده اینجا هم اعمال می‌شود.

    خروجی list است نه zip: در ویو دو بار روی همین مقدار پیمایش می‌شود و zip
    یک‌بارمصرف است.
    """
    tours_by_city = {}

    direct = Tour.objects.filter(
        PubTour=True, Tcity__CountryName_id=country_id
    ).values_list('Tcity_id', 'id')
    for city_id, tour_id in direct:
        tours_by_city.setdefault(city_id, set()).add(tour_id)

    related = related_tour_city.objects.filter(
        tour__PubTour=True, city__CountryName_id=country_id
    ).values_list('city_id', 'tour_id')
    for city_id, tour_id in related:
        tours_by_city.setdefault(city_id, set()).add(tour_id)

    if not tours_by_city:
        return []

    cities = City.objects.filter(id__in=tours_by_city.keys()).select_related('CountryName')
    return [(c, len(tours_by_city[c.id])) for c in cities]

def get_origin_tours(origin_id):
    return Tour.objects.filter(origin_city=origin_id)

def get_origin_menu_cities(origin_id):
    tours_cities_name = []
    tours_cities_id = []
    tours_cities_slug = []
    for i in get_origin_tours(origin_id):
        tours_cities_name.append(i.Tcity.Name)
    tours_cities_name = sorted(list(set(tours_cities_name)))
    for i in tours_cities_name:
        city_data = City.objects.get(Name=i)
        tours_cities_id.append(city_data.id)
        tours_cities_slug.append(city_data.slug)
    menu_cities = zip(tours_cities_name, tours_cities_slug, tours_cities_id)
    return menu_cities

def get_norooz_tours():
    tours = Tour.objects.filter(PubTour=True, norooz=True).select_related('Tcountry', 'Tcity', 'origin_city').order_by('-id')
    return tours

def get_norooz_tours_cities():
    tours = list(get_norooz_tours())
    bulk = tour_cities_bulk(tours)
    return [bulk.get(t.id, []) for t in tours]

def get_norooz_tours_packages():
    tours = list(get_norooz_tours())
    bulk = tour_card_packages_bulk(tours)
    return [bulk.get(t.id, []) for t in tours]

def get_installment_tours():
    tours = Tour.objects.filter(PubTour=True, Installment=True).select_related('Tcountry', 'Tcity', 'origin_city').order_by('-id')
    return tours

def get_installment_tours_cities():
    tours = list(get_installment_tours())
    bulk = tour_cities_bulk(tours)
    return [bulk.get(t.id, []) for t in tours]

def get_installment_tours_packages():
    tours = list(get_installment_tours())
    bulk = tour_card_packages_bulk(tours)
    return [bulk.get(t.id, []) for t in tours]

def get_all_hotels():
    return Hotel_Data.objects.all()

def get_all_gte_hotels():
    return get_all_hotels().filter(satrap_gte=True)

def get_all_price_hotels():
    return get_all_hotels().filter(hotel_price__isnull=False)



def get_all_city_hotels(city_id):
    hotels = Hotel_Data.objects.filter(Hcity=city_id).order_by('-id')
    return hotels

def get_all_country_hotels(country_id):
    hotels = Hotel_Data.objects.filter(Hcountry=country_id).order_by('-id')
    return hotels

def get_hotel_countries_hotel_count():
    hotel_number = []
    countries = Country.objects.filter(hotel_country__isnull=False).distinct()
    for i in countries:
        hotel_num = Hotel_Data.objects.filter(Hcountry=i).count()
        hotel_number.append(hotel_num)
    return zip(countries, hotel_number)

def get_hotel_cities_hotel_count(country_id):
    cities = set()
    hotel_number = []
    for i in get_all_country_hotels(country_id):
        cities.add(i.Hcity)
    for i in cities:
        hotel_num = Hotel_Data.objects.filter(Hcity=i).count()
        hotel_number.append(hotel_num)
    return zip(cities, hotel_number)

def get_all_hotels_cities():
    all_cities = cache.get('cities_with_hotel')
    print('cached-data')
    if not all_cities:
        all_cities = City.objects.filter(hotel_city__isnull=False).order_by('-id').distinct()
        cache.set('cities_with_hotel', all_cities, timeout=1800)
    return all_cities

def get_top_pages():
    return pages.objects.filter(reseller=True)

def get_all_order():
    orders = TourOrder.objects.all().order_by('-OrderTime')
    return orders

def get_all_memories():
    memories = PMemories.objects.all().order_by('-id')
    return memories

def get_all_contacts_msg():
    allmsg = ContactUs.objects.all().order_by('-id')
    return allmsg

def get_all_airport():
    airport = Airport.objects.all().order_by('-id')
    return airport

def get_all_post_categories():
    categories = PostCategory.objects.all().order_by('-id')
    return categories

def get_all_memos_categories():
    categories = MemoryCategory.objects.all().order_by('-id')
    return categories

def get_all_tour_categories():
    categories = CustomTourCategory.objects.all().order_by('-id')
    return categories

def get_pub_tour_airlines():
    cities = []
    airlines = []
    tours = list(get_all_pub_tours())
    first_city = {}
    for tour_city in TourCity.objects.filter(TourName__in=tours).select_related('Airline').order_by('id'):
        first_city.setdefault(tour_city.TourName_id, tour_city)
    for i in tours:
        cities.append(first_city.get(i.id))
    for i in cities:
        if i is not None:
            airlines.append(i.Airline)
    airlines = list(set(airlines))
    return airlines

def get_all_tour_trip_plans(tour_id):
    tour_trip_plans = TripPlan.objects.filter(tour=tour_id).order_by('id')
    return tour_trip_plans


def get_country_memory_category(country):
    if country is None:
        return None

    ck = 'memo_cat_for_country_%s' % country.id
    hit = cache.get(ck)
    if hit is not None:
        return hit or None

    from django.db.models import Q
    from tour.models import MemoryCategory, PMemories

    slug = (country.slug or '').strip().lower()
    title = (country.TitleC or '').strip()

    cat = None
    if slug:
        cat = MemoryCategory.objects.filter(
            parentCat__isnull=True, slug__iexact=slug).first()
    if cat is None and title:
        cat = MemoryCategory.objects.filter(
            parentCat__isnull=True, CatName__icontains=title).first()
    if cat is None:
        cache.set(ck, '', 60 * 30)
        return None

    total = PMemories.objects.filter(publish=True).filter(
        Q(category=cat) | Q(category__parentCat=cat)).count()
    if not total:
        cache.set(ck, '', 60 * 30)
        return None

    data = {'slug': cat.slug, 'name': cat.CatName, 'count': total}
    cache.set(ck, data, 60 * 30)
    return data
