from django.core.paginator import Paginator
from django.shortcuts import render
from blog.dataset import get_all_blog_posts
from tour.dataset import *
from tour.models import *


def ajax_hotel_list(request):
    hotellist = get_all_hotels().order_by('-id')
    if 'hotel_name' in request.GET:
        hotel_name = request.GET['hotel_name']
        if hotel_name:
            hotellist = hotellist.filter(HotelName__contains=hotel_name).order_by('-id')
    if 'hotel_name_eng' in request.GET:
        hotel_name_eng = request.GET['hotel_name_eng']
        if hotel_name_eng:
            hotellist = hotellist.filter(HotelNameEnglish__contains=hotel_name_eng).order_by('-id')
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            city = City.objects.get(id=city)
            hotellist = hotellist.filter(Hcity=city).order_by('-id')
    paginator = Paginator(hotellist, 20)
    page_number = request.GET.get('page')
    hotellist = paginator.get_page(page_number)
    context = {
        'Hotels': hotellist,
    }
    return render(request, 'hotel/ajax-hotels-list.html', context)


def ajax_hotel_cities(request):
    cities = Hotel_Data.objects.values_list('Hcity', flat=True).distinct()
    cities_data = []
    for i in cities:
        cities_data.append(City.objects.get(id=i))
    context = {
        'cities': cities_data
    }
    return render(request, 'hotel/hotel_cities.html', context)


def ajax_airline_list(request):
    airlines = get_airline_list()
    paginator = Paginator(airlines, 10)
    page = request.GET.get('page')
    airline_list = paginator.get_page(page)
    context = {
        'AirlinesList': airline_list
    }
    return render(request, 'ajax/airline_list.html', context)


def ajax_country_list(request):
    countries = get_all_country().order_by('-id')
    paginator = Paginator(countries, 15)
    page = request.GET.get('page')
    countries_list = paginator.get_page(page)
    context = {
        'countries': countries_list
    }
    return render(request, 'ajax/country_list.html', context)


def ajax_city_list(request):
    cities = get_all_city().order_by('-id')
    country_name = request.GET.get('country_name')
    city_name = request.GET.get('city_name')
    if country_name:
        country = Country.objects.filter(TitleC__contains=country_name)
        if len(country) > 0:
            cities = get_all_city().filter(CountryName=country[0]).order_by('-id')
    if city_name:
        cities = get_all_city().filter(Name__icontains=city_name).order_by('-id')
    paginator = Paginator(cities, 15)
    page = request.GET.get("page")
    cities_list = paginator.get_page(page)
    context = {
        'cities': cities_list
    }
    return render(request, 'ajax/city_list.html', context)

def ajax_city_media_list(request):
    country_id = request.GET.get('country_id')
    media_list = get_all_city_media(country_id)
    paginator = Paginator(media_list, 5)
    page = request.GET.get('page')
    media_list = paginator.get_page(page)
    context = {
        'media_list': media_list
    }
    return render(request, 'ajax/city_media.html', context)

def ajax_country_media_list(request):
    country_id = request.GET.get('country_id')
    media_list = get_all_country_media(country_id)
    paginator = Paginator(media_list, 5)
    page = request.GET.get('page')
    media_list = paginator.get_page(page)
    context = {
        'media_list': media_list
    }
    return render(request, 'ajax/country_media.html', context)

def ajax_country_faq_list(request):
    country_id = request.GET.get('country_id')
    faq_list = get_all_country_faq(country_id)
    paginator = Paginator(faq_list, 5)
    page = request.GET.get('page')
    faq_list = paginator.get_page(page)
    context = {
        'faq_list': faq_list
    }
    return render(request, 'ajax/country_faq.html', context)

def ajax_country_hotel_faq_list(request):
    country_id = request.GET.get('country_id')
    faq_list = hotel_faq_Country.objects.filter(Countryfaq=country_id)
    paginator = Paginator(faq_list, 5)
    page = request.GET.get('page')
    faq_list = paginator.get_page(page)
    context = {
        'faq_list': faq_list
    }
    return render(request, 'ajax/country_hotel_faq.html', context)


def ajax_city_faq_list(request):
    city_id = request.GET.get('city_id')
    faq_list = get_all_city_faq(city_id)
    paginator = Paginator(faq_list, 5)
    page = request.GET.get('page')
    faq_list = paginator.get_page(page)
    context = {
        'faq_list': faq_list
    }
    return render(request, 'ajax/city_faq.html', context)

def ajax_city_hotel_faq_list(request):
    city_id = request.GET.get('city_id')
    faq_list = hotel_faq_city.objects.filter(Cityfaq=city_id)
    paginator = Paginator(faq_list, 5)
    page = request.GET.get('page')
    faq_list = paginator.get_page(page)
    context = {
        'faq_list': faq_list
    }
    return render(request, 'ajax/city_hotel_faq.html', context)


def ajax_tour_list(request):
    tours = get_all_tours()
    cities = []
    if 'tourname' in request.GET:
        tourname = request.GET['tourname']
        tours = tours.filter(Title__icontains=tourname)
    if 'startdate' in request.GET:
        startdate = request.GET['startdate']
        if startdate != '':
            tours = tours.filter(StartDate=startdate)
    if 'enddate' in request.GET:
        enddate = request.GET['enddate']
        if enddate != '':
            tours = tours.filter(EndDate=enddate)
    if 'tour_stat' in request.GET:
        tour_stat = request.GET['tour_stat']
        if tour_stat == '1':
            tours = tours.filter(PubTour=True)
        if tour_stat == '0':
            tours = tours.filter(PubTour=False)
    for i in tours:
        cities.append(TourCity.objects.filter(TourName_id=i.id))
    paginator = Paginator(tours, 10)
    page_number = request.GET.get('page')
    tour_list = paginator.get_page(page_number)
    paginator2 = Paginator(cities, 10)
    page_number2 = request.GET.get('page')
    cities = paginator2.get_page(page_number2)
    alldata = list(zip(tour_list, cities))
    context = {
        'data': alldata,
        'tour_list': tour_list
    }
    return render(request, 'ajax/all_tour_list.html', context)


def ajax_posts_list(request):
    all_posts = get_all_blog_posts()
    post_category = request.GET.get('post_category')
    if post_category:
        all_posts = all_posts.filter(Category=post_category)
    active = request.GET.get('active')
    if active == '1':
        all_posts = all_posts.filter(Publish=True)
    if active == '0':
        all_posts = all_posts.filter(Publish=False)
    post_title = request.GET.get('post_title')
    if post_title:
        all_posts = all_posts.filter(Title__contains=post_title)
    paginator = Paginator(all_posts, 20)
    page_number = request.GET.get('page')
    all_posts = paginator.get_page(page_number)
    context = {
        'all_posts': all_posts
    }
    return render(request, 'ajax/all_post_list.html', context)


def ajax_order_list(request):
    orders = get_all_order()
    mobile = request.GET.get('mobile')
    if mobile:
        orders = orders.filter(Mobile=mobile)
    trs_code = request.GET.get('trs_code')
    if trs_code:
        orders = orders.filter(OrderCode=trs_code)
    view = request.GET.get('view')
    if view == '1':
        orders = orders.filter(View=True)
    if view == '0':
        orders = orders.filter(View=False)
    paginator = Paginator(orders, 20)
    page_number = request.GET.get('page')
    orders = paginator.get_page(page_number)
    context = {
        'orders': orders
    }
    return render(request, 'ajax/ajax_order_list.html', context)


def ajax_memories_list(request):
    memories = get_all_memories()
    mobile = request.GET.get('mobile')
    if mobile:
        memories = memories.filter(Mobile=mobile)
    email = request.GET.get('email')
    if email:
        memories = memories.filter(Email=email)
    memo_stat = request.GET.get('memo_stat')
    if memo_stat == '1':
        memories = memories.filter(publish=True)
    if memo_stat == '0':
        memories = memories.filter(publish=False)
    paginator = Paginator(memories, 10)
    page_number = request.GET.get('page')
    memories = paginator.get_page(page_number)
    context = {
        'memories': memories
    }
    return render(request, 'ajax/ajax_memories_list.html', context)


def ajax_allmsg_list(request):
    allmsg = get_all_contacts_msg()
    paginator = Paginator(allmsg, 20)
    page_number = request.GET.get('page')
    allmsg = paginator.get_page(page_number)
    context = {
        'allmsg': allmsg
    }
    return render(request, 'ajax/ajax_msg_list.html', context)


def ajax_airpots_list(request):
    airpots = get_all_airport()
    paginator = Paginator(airpots, 10)
    pagenumber = request.GET.get('page')
    airpots = paginator.get_page(pagenumber)
    context = {
        'airpots': airpots
    }
    return render(request, 'ajax/ajax_airport_list.html', context)


def ajax_post_categories(request):
    categories = get_all_post_categories()
    paginator = Paginator(categories, 10)
    page_number = request.GET.get('page')
    categories = paginator.get_page(page_number)
    context = {
        'categories': categories
    }
    return render(request, 'ajax/ajax_categories_list.html', context)


def ajax_memo_categories(request):
    categories = get_all_memos_categories()
    paginator = Paginator(categories, 10)
    page_number = request.GET.get('page')
    categories = paginator.get_page(page_number)
    context = {
        'categories': categories
    }
    return render(request, 'ajax/ajax_memo_categories_list.html', context)


def ajax_tour_categories(request):
    categories = get_all_tour_categories()
    paginator = Paginator(categories, 10)
    page_number = request.GET.get('page')
    categories = paginator.get_page(page_number)
    
    context = {
        'categories': categories
    }
    return render(request, 'ajax/ajax_list_tour_categories.html', context)


def ajax_main_packages_list(request):
    main_packages = MainPackage.objects.all().order_by('-id')
    paginator = Paginator(main_packages, 10)
    page_number = request.GET.get('page')
    main_packages = paginator.get_page(page_number)
    context = {
        'MainPackages': main_packages
    }
    return render(request, 'ajax/ajax_main-package-list.html', context)


def ajax_trip_plans(request):
    tour_id = request.GET.get('tour_id')
    trip_plans = get_all_tour_trip_plans(tour_id)
    paginator = Paginator(trip_plans, 10)
    page_number = request.GET.get('page')
    trip_plans = paginator.get_page(page_number)
    context = {
        'trip_plans': trip_plans
    }
    return render(request, 'ajax/ajax_trip_palns.html', context)
