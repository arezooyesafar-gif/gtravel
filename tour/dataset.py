from operator import attrgetter
from django.core.paginator import Paginator
from blog.models import blogPosts, PostCategory
from hotels.models import Hotel_Data
from .models import *
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
    pub_tours = Tour.objects.filter(PubTour=True).order_by('-updateDate')
    return pub_tours

def get_all_pub_tours_dates():
    dates = date_plan.objects.all()
    return dates

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

def get_all_tours_cities_data():
    tours_cities = []
    tours = get_all_tours()
    for i in tours:
        tours_cities.append(TourCity.objects.filter(TourName_id=i.id))
    return tours_cities

def get_tours_cities_data():
    tours_cities = []
    tours = get_all_pub_tours()
    for i in tours:
        tours_cities.append(TourCity.objects.filter(TourName_id=i.id))
    return tours_cities

def get_tours_packages_data():
    tours_packages = []
    tours = get_all_pub_tours()
    for i in tours:
        packages = Package.objects.filter(TourName_id=i.id).order_by('DoubleBedPrice', 'DoubleBedPrice_doller')
        if packages.exists():
            tours_packages.append([packages.first()])
        else:
            tours_packages.append([])
    return tours_packages

def get_spacial_tours():
    spacial_tours = Tour.objects.filter(Feature=True, PubTour=True).only('Title', 'NightCount', 'TourImage')
    spacial_packages = [
        Package.objects.filter(TourName_id=tour_id).only('DoubleBedPrice', 'Pcry').order_by(
            'DoubleBedPrice', 'DoubleBedPrice_doller') for tour_id in spacial_tours
    ]
    spacial_cities = [TourCity.objects.filter(TourName_id=tour_id).only('Airline', 'TourName_id')
               for tour_id in spacial_tours]
    spacialData = zip(spacial_tours, spacial_cities, spacial_packages)
    return spacialData

def get_all_pub_posts():
    return blogPosts.objects.filter(Publish=True).only('Title').order_by('-id')

def get_menu_cities():
    tours_cities_name = []
    tours_cities_slug = []
    for i in get_all_pub_tours_admin():
        tours_cities_name.append(i.Tcity.Name)
    tours_cities_name = sorted(list(set(tours_cities_name)))
    for i in tours_cities_name:
        city_data = City.objects.get(Name=i)
        tours_cities_slug.append(city_data.slug)
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
    countries = []
    countries_tours = []
    for i in Tour.objects.filter(PubTour=True).order_by('-id'):
        countries.append(i.Tcountry)
    countries = list(set(countries))
    for i in countries:
        tour_num = Tour.objects.filter(Tcountry=i, PubTour=True).count()
        if tour_num:
            countries_tours.append(tour_num)
    tour_countries = zip(countries, countries_tours)
    return tour_countries

def get_tours_cities():
    cities = []
    for i in Tour.objects.filter(PubTour=True).order_by('-id'):
        cities.append(i.Tcity)
    cities = list(set(cities))
    return cities

def get_airlines():
    airlines = AirLineData.objects.all()
    return airlines

def get_tours_country_list():
    countries = Country.objects.filter(tocountry__PubTour=True).order_by('menu_order').distinct()
    return countries

def get_country_tours(country_id):
    tour_list = []
    tours_query = related_tour_city.objects.filter(country=country_id, tour__PubTour=True)
    tours_query = list(set(tours_query))
    for i in tours_query:
        tour_list.append(i.tour)
    tour_list = list(set(tour_list))
    tour_list = sorted(tour_list, key=attrgetter('updateDate'))
    return tour_list

def get_city_tours(city_id):
    tour_list = []
    tours_query = related_tour_city.objects.filter(city=city_id, tour__PubTour=True)
    tours_query = list(set(tours_query))
    for i in tours_query:
        tour_list.append(i.tour)
    tour_list = list(set(tour_list))
    tour_list = sorted(tour_list, key=attrgetter('updateDate'))
    return tour_list

def get_city_tours_cities(city_id):
    cities = []
    tours = get_city_tours(city_id)
    for i in tours:
        cities.append(TourCity.objects.filter(TourName=i))
    return cities

def get_city_tours_packages(city_id):
    packages = []
    tours = get_city_tours(city_id)
    for i in tours:
        packages.append(Package.objects.filter(TourName_id=i.id).order_by('DoubleBedPrice', 'DoubleBedPrice_doller'))
    return packages

def get_country_tours_cities(country_id):
    cities = []
    tours = get_country_tours(country_id)
    for i in tours:
        cities.append(TourCity.objects.filter(TourName=i))
    return cities

def get_country_tours_packages(country_id):
    packages = []
    tours = get_country_tours(country_id)
    for i in tours:
        packages.append(Package.objects.filter(TourName_id=i.id).order_by('DoubleBedPrice', 'DoubleBedPrice_doller'))
    return packages

def get_country_tours_datePlan(country_id):
    datePlan = []
    tours = get_country_tours(country_id)
    for i in tours:
        datePlan.append(date_plan.objects.filter(tour=i).count())
    return datePlan

def get_contry_cities(country_id):
    unique_city_names = set()
    country_cities_tours = []
    tours = get_country_tours(country_id)
    for tour in tours:
        unique_city_names.add(tour.Tcity.Name)
    country_cities = City.objects.filter(Name__in=unique_city_names)
    for i in country_cities:
        tour_num = Tour.objects.filter(Tcity_id=i, PubTour=True).count()
        if tour_num:
            country_cities_tours.append(tour_num)
    return zip(country_cities, country_cities_tours)

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
    tours = Tour.objects.filter(PubTour=True, norooz=True).order_by('-id')
    return tours

def get_norooz_tours_cities():
    cities = []
    for i in get_norooz_tours():
        cities.append(TourCity.objects.filter(TourName_id=i.id))
    return cities

def get_norooz_tours_packages():
    packages = []
    for i in get_norooz_tours():
        packages.append(Package.objects.filter(TourName_id=i.id).order_by('DoubleBedPrice'))
    return packages

def get_installment_tours():
    tours = Tour.objects.filter(PubTour=True, Installment=True).order_by('-id')
    return tours

def get_installment_tours_cities():
    cities = []
    for i in get_installment_tours():
        cities.append(TourCity.objects.filter(TourName_id=i.id))
    return cities

def get_installment_tours_packages():
    packages = []
    for i in get_installment_tours():
        packages.append(Package.objects.filter(TourName_id=i.id).order_by('DoubleBedPrice'))
    return packages

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

def get_pub_tour_airlines():
    cities = []
    airlines = []
    tours = get_all_pub_tours()
    for i in tours:
        cities.append(TourCity.objects.filter(TourName=i).first())
    for i in cities:
        airlines.append(i.Airline)
    airlines = list(set(airlines))
    return airlines

def get_all_tour_trip_plans(tour_id):
    tour_trip_plans = TripPlan.objects.filter(tour=tour_id)
    return tour_trip_plans
