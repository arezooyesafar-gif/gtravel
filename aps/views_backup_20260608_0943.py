import json
import random
import string
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from django.db import models as M
from hotels.forms import hotel_comment_form
from hotels.models import Hotel_Data, hotel_images, hotel_comments
from person.models import profile
from tour.dataset import *
from django.contrib import messages
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect
from theme.models import index_page
from tour.forms import SearchForm, ContactUsForm, SubscribeForm, reservsionCreateForm, createOrderDoc
from pages.dataset import *
from visa.forms import visa_request_form, thaiVisaForm
from blog.models import *
from django.shortcuts import get_object_or_404, render

def IndexPage(request):
    date = datetime.now()
    date = date.date()
    ArchiveTour = Tour.objects.filter(StartDate=date)
    for tour in ArchiveTour:
        tour.PubTour = False
        tour.save()
    items = spacial_destinations.objects.filter(show_homepage=True)
    theme_setting = index_page.objects.get(id=1)
    view = viewCounter.objects.get(id=1)
    view.indexView += 1
    view.save()
    all_faqs = faq_home.objects.all()
    countries = get_tours_country()
    select_countries = Country.objects.all()
    tours_country_list = get_tours_country_list()
    spacialTours = get_spacial_tours()
    forms = SearchForm()
    formsub = SubscribeForm()
    top_menu = TourMenu.objects.filter(show_meu=True)
    if request.method == 'POST':
        formsub = SubscribeForm(request.POST)
        if formsub.is_valid():
            formsub.save()
            return redirect('/')
    context = {
        'all_faqs': all_faqs,
        'Search': forms,
        'Sub': formsub,
        'set': theme_setting,
        'countries': countries,
        'tour_countries': tours_country_list,
        'SpacialData': spacialTours,
        'select_countries': select_countries,
        'spacialDest': items,
        'top_menu': top_menu,
        }
    return render(request, 'ui/index.html', context)

def ajax_dest(request):
    dest = request.GET.get('DestCountry')
    dest_list = []
    if dest != '':
        ctry = Country.objects.filter(TitleC__contains=dest)
        cty = City.objects.filter(Name__contains=dest)
        for i in ctry:
            dest_list.append(i.TitleC)
        for i in cty:
            dest_list.append(i.Name)
        context = {
            'dest': dest_list
        }
        return render(request, 'ui/ajax_dest.html', context)
    if not dest:
        dest_list = []
        context = {
            'dest': dest_list
        }
        return render(request, 'ui/ajax_dest.html', context)

def CategoryTourList(request, slug, id):
    try:
        menu = Country.objects.get(slug=slug)
    except Country.DoesNotExist:
        raise Http404
    reseller_menu = get_top_pages()
    footer_2 = get_colm_two_pages()
    footer_3 = get_colm_tree_pages()
    tours_country_list = get_tours_country_list()
    contry_cities = get_contry_cities(menu.id)
    contry_cities_post = get_contry_cities(menu.id)
    faqs = FAQ.objects.filter(Countryfaq=menu.id)
    forms = SearchForm()
    theme_setting = index_page.objects.get(id=1)
    airlines = get_airlines()
    dest_cities = City.objects.filter(CountryName=menu)
    country_media = CityCountryMedia.objects.filter(country_id=id, is_active=True).order_by('sort_order', '-created_at')
    items = spacial_destinations.objects.filter(show_homepage=True)
    meta_robots = menu.tour_meta_robots

    tourlist = get_country_tours(menu.id)

    page_number = request.GET.get('page', 1)
    paginator = Paginator(tourlist, 9)
    tourlist = paginator.get_page(page_number)

    packages = []
    tour_cities = []
    dates = []

    for tour in tourlist:
        packages.append(
        Package.objects.filter(TourName=tour).order_by('DoubleBedPrice')
        )

        tour_cities.append(
        TourCity.objects.filter(TourName=tour)
        )

        dates.append(
        date_plan.objects.filter(tour=tour).count()
       )

    alldata = list(zip(tourlist, packages, tour_cities, dates))

    context = {
        'reseller_menu': reseller_menu,
        'Search': forms,
        'all_faqs': faqs,
        'country': menu,
        'set': theme_setting,
        'cities': contry_cities,
        'cities_post': contry_cities_post,
        'footer_2': footer_2,
        'footer_3': footer_3,
        'tour_countries': tours_country_list,
        'dest_cities': dest_cities,
        'airlines': airlines,
        'spacialDest': items,
        'media_list': country_media,
        'meta_robots': meta_robots,
        'pubTours': alldata,
        'tours_list': tourlist,
    }
    return render(request, 'ui/all-tour.html', context)

def CityTourListOrigin(request, id, slug):
    reseller_menu = get_top_pages()
    cities_menu = get_menu_cities()
    footer_2 = get_colm_two_pages()
    footer_3 = get_colm_tree_pages()
    orgin_menu_cities = get_origin_menu_cities(69)
    theme_setting = index_page.objects.get(id=1)
    try:
        menu = City.objects.get(id=id, slug=slug)
    except City.DoesNotExist:
        raise Http404
    faqs = cityFAQ.objects.filter(Cityfaq=menu)
    tours = Tour.objects.filter(Tcity=menu.id, PubTour=True, origin_city=69).order_by('-updateDate')
    cities = []
    for i in tours:
        cities.append(TourCity.objects.filter(TourName_id=i))
    paginator = Paginator(tours, 10)
    PageNumber = request.GET.get('page')
    tours = paginator.get_page(PageNumber)
    packages = []
    for i in tours:
        packages.append(Package.objects.filter(TourName_id=i.id).order_by('DoubleBedPrice'))
    alldata = zip(tours, cities, packages)
    forms = SearchForm()
    context = {
        'reseller_menu': reseller_menu,
        'AllTour': tours,
        'AllData': alldata,
        'Search': forms,
        'Menu': menu,
        'all_faqs': faqs,
        'set': theme_setting,
        'tours_cities_list': cities_menu,
        'orgin_menu_cities': orgin_menu_cities,
        'footer_2': footer_2,
        'footer_3': footer_3,
    }
    return render(request, 'ui/all-tour.html', context)

def CityTourList(request,slug, id):
    items = spacial_destinations.objects.filter(show_homepage=True)
    tours_country_list = get_tours_country_list()
    airlines = AirLineData.objects.all()
    footer_2 = get_colm_two_pages()
    footer_3 = get_colm_tree_pages()
    theme_setting = index_page.objects.get(id=1)
    city_media = CityCountryMedia.objects.filter(city_id = id, is_active = True).order_by('sort_order', '-created_at')
    try:
        menu = City.objects.get(slug=slug)
    except City.DoesNotExist:
        raise Http404
    faqs = cityFAQ.objects.filter(Cityfaq=menu)
    forms = SearchForm()
    meta_robots = menu.tour_meta_robots

    tourlist = get_city_tours(menu.id)
    page_number = request.GET.get('page', 1)
    paginator = Paginator(tourlist, 9)
    tourlist = paginator.get_page(page_number)
    packages = []
    tour_cities = []
    dates = []
    for tour in tourlist:
        packages.append(
         Package.objects.filter(TourName=tour).order_by('DoubleBedPrice')
        )

        tour_cities.append(
         TourCity.objects.filter(TourName=tour)
        )

        dates.append(
         date_plan.objects.filter(tour=tour).count()
        )
    alldata = list(zip(tourlist, packages, tour_cities, dates))

    context = {
        'Search': forms,
        'city': menu,
        'media_list': city_media,
        'all_faqs': faqs,
        'set': theme_setting,
        'footer_2': footer_2,
        'footer_3': footer_3,
        'tour_countries': tours_country_list,
        'spacialDest': items,
        'airlines': airlines,
        'meta_robots': meta_robots,
        'pubTours': alldata,
        'tours_list': tourlist,
    }
    return render(request, 'ui/all-tour.html', context)

def AllTourList(request):
    items_tour = spacial_destinations.objects.filter(show_tourpage=True)
    items = spacial_destinations.objects.filter(show_homepage=True)
    view = viewCounter.objects.get(id=1)
    view.toursView += 1
    view.save()
    tours_country_list = get_tours_country_list()
    reseller_menu = get_top_pages()
    footer_2 = get_colm_two_pages()
    footer_3 = get_colm_tree_pages()
    countries = get_tours_country()
    dest_cities = get_tours_cities
    airlines = get_pub_tour_airlines()
    forms = SearchForm()
    all_faqs = faq_home.objects.all()
    theme_setting = index_page.objects.get(id=1)
    meta_robots = 'INDEX,FOLLOW'

    tourlist = get_all_pub_tours()
    page_number = request.GET.get('page', 1)
    paginator = Paginator(tourlist, 9)
    tourlist = paginator.get_page(page_number)
    packages = []
    tour_cities = []
    dates = []
    for tour in tourlist:
        packages.append(
         Package.objects.filter(TourName=tour).order_by('DoubleBedPrice')
        )
        tour_cities.append(
         TourCity.objects.filter(TourName=tour)
        )
        dates.append(
            date_plan.objects.filter(tour=tour).count()
        )
    alldata = list(zip(tourlist, packages, tour_cities, dates))

    context = {
        'reseller_menu': reseller_menu,
        'Search': forms,
        'all_faqs': all_faqs,
        'set': theme_setting,
        'countries': countries,
        'footer_2': footer_2,
        'footer_3': footer_3,
        'tour_countries': tours_country_list,
        'dest_cities': dest_cities,
        'airlines': airlines,
        'spacialDest': items,
        'spacialDest_tour': items_tour,
        'meta_robots': meta_robots,
        'pubTours': alldata,
        'tours_list': tourlist,
    }
    return render(request, 'ui/all-tour.html', context)

def MenuTourList(request, slug):
    try:
        menu = TourMenu.objects.get(slug=slug)
    except TourMenu.DoesNotExist:
        raise Http404
    top_menu = TourMenu.objects.filter(show_meu=True)
    items = spacial_destinations.objects.filter(show_homepage=True)
    items_2 = spacial_destinations.objects.filter(show_homepage=True)
    countries = get_tours_country()
    dest_cities = get_tours_cities
    airlines = get_pub_tour_airlines()
    forms = SearchForm()
    formsub = SubscribeForm()
    if request.method == 'POST':
        formsub = SubscribeForm(request.POST)
        if formsub.is_valid():
            formsub.save()
            return redirect('/')
    context = {
        'dest_cities': dest_cities,
        'countries': countries,
        'airlines': airlines,
        'Search': forms,
        'Menu': menu,
        'Sub': formsub,
        'top_menu': top_menu,
        'spacialDest': items,
        'spacialDest_tour': items_2,
    }
    return render(request, 'ui/all-tour-list-city.html', context)

def tour_category_detail(request, slug):
    category = get_object_or_404(
        CustomTourCategory,
        slug=slug
    )
    faqs = TourCategoryFAQ.objects.filter(category=category)

    context = {
        'category': category,
        'category_title': category.name,
        'category_desc': category.description,
        'countries': get_tours_country(),
        'tour_countries': get_tours_country_list(),
        'dest_cities': get_tours_cities(),
        'airlines': get_pub_tour_airlines(),
        'spacialDest': spacial_destinations.objects.filter(show_homepage=True),
        'spacialDest_tour': spacial_destinations.objects.filter(show_tourpage=True),
        'all_faqs': faqs,
        'meta_robots': category.meta_robots,
    }
    return render(
        request,
        'ui/all-tour.html',
        context
    )

def AllTourList_norooz(request):
    reseller_menu = get_top_pages()
    cities_menu = get_menu_cities()
    footer_2 = get_colm_two_pages()
    footer_3 = get_colm_tree_pages()
    orgin_menu_cities = get_origin_menu_cities(69)
    view = viewCounter.objects.get(id=1)
    view.toursView += 1
    view.save()
    cities = get_norooz_tours_cities()
    packages = get_norooz_tours_packages()
    tours = get_norooz_tours()
    countries = get_tours_country()
    paginator = Paginator(tours, 10)
    pagenumber = request.GET.get('page')
    tours = paginator.get_page(pagenumber)
    paginator2 = Paginator(cities, 10)
    pagenumber2 = request.GET.get('page')
    cities = paginator2.get_page(pagenumber2)
    paginator3 = Paginator(packages, 10)
    pagenumber3 = request.GET.get('page')
    packages = paginator3.get_page(pagenumber3)
    alldata = zip(tours, cities, packages)
    menus = Country.objects.filter(showInMenu=True)
    forms = SearchForm()
    all_faqs = faq_home.objects.all()
    theme_setting = index_page.objects.get(id=1)
    context = {
        'reseller_menu': reseller_menu,
        'orgin_menu_cities': orgin_menu_cities,
        'tours_cities_list': cities_menu,
        'AllTour': tours,
        'AllData': alldata,
        'Search': forms,
        'Tours': tours,
        'menus': menus,
        'all_faqs': all_faqs,
        'set': theme_setting,
        'countries': countries,
        'footer_2': footer_2,
        'footer_3': footer_3,
    }
    if request.user_agent.is_mobile:
        return render(request, 'ui/mobile/all-tour-norooz.html', context)
    else:
        return render(request, 'ui/all-tour-norooz.html', context)

def AllTourList_Installment(request):
    reseller_menu = get_top_pages()
    cities_menu = get_menu_cities()
    footer_2 = get_colm_two_pages()
    footer_3 = get_colm_tree_pages()
    orgin_menu_cities = get_origin_menu_cities(69)
    view = viewCounter.objects.get(id=1)
    view.toursView += 1
    view.save()
    cities = get_installment_tours_cities()
    packages = get_installment_tours_packages()
    tours = get_installment_tours()
    countries = get_tours_country()
    paginator = Paginator(tours, 10)
    pagenumber = request.GET.get('page')
    tours = paginator.get_page(pagenumber)
    paginator2 = Paginator(cities, 10)
    pagenumber2 = request.GET.get('page')
    cities = paginator2.get_page(pagenumber2)
    paginator3 = Paginator(packages, 10)
    pagenumber3 = request.GET.get('page')
    packages = paginator3.get_page(pagenumber3)
    alldata = zip(tours, cities, packages)
    menus = Country.objects.filter(showInMenu=True)
    forms = SearchForm()
    all_faqs = faq_home.objects.all()
    theme_setting = index_page.objects.get(id=1)
    context = {
        'reseller_menu': reseller_menu,
        'orgin_menu_cities': orgin_menu_cities,
        'tours_cities_list': cities_menu,
        'AllTour': tours,
        'AllData': alldata,
        'Search': forms,
        'Tours': tours,
        'menus': menus,
        'all_faqs': all_faqs,
        'set': theme_setting,
        'countries': countries,
        'footer_2': footer_2,
        'footer_3': footer_3,
    }
    if request.user_agent.is_mobile:
        return render(request, 'ui/mobile/all-tour-install.html', context)
    else:
        return render(request, 'ui/all-tour-install.html', context)

def all_tour_list_origins(request, slug, id):
    reseller_menu = get_top_pages()
    cities_menu = get_menu_cities()
    footer_2 = get_colm_two_pages()
    footer_3 = get_colm_tree_pages()
    orgin_menu_cities = get_origin_menu_cities(69)
    theme_setting = index_page.objects.get(id=1)
    try:
        menu = City.objects.get(id=id, slug=slug)
    except City.DoesNotExist:
        raise Http404
    faqs = cityFAQ.objects.filter(Cityfaq=menu)
    tours = Tour.objects.filter(origin_city=menu.id, PubTour=True).order_by('-updateDate')
    cities = []
    for i in tours:
        cities.append(TourCity.objects.filter(TourName_id=i))
    paginator = Paginator(tours, 10)
    PageNumber = request.GET.get('page')
    tours = paginator.get_page(PageNumber)
    packages = []
    for i in tours:
        packages.append(Package.objects.filter(TourName_id=i.id).order_by('DoubleBedPrice'))
    alldata = zip(tours, cities, packages)
    forms = SearchForm()
    tours = Tour.objects.filter(PubTour=True).order_by('-id')
    origins = []
    origin_tours = []
    for i in tours:
        origins.append(i.origin_city)
    origins = list(set(origins))
    for i in origins:
        tour_num = Tour.objects.filter(origin_city=i, PubTour=True).count()
        if tour_num:
            origin_tours.append(tour_num)
    context = {
        'reseller_menu': reseller_menu,
        'orgin_menu_cities': orgin_menu_cities,
        'tours_cities_list': cities_menu,
        'AllTour': tours,
        'AllData': alldata,
        'Search': forms,
        'Menu': menu,
        'all_faqs': faqs,
        'set': theme_setting,
        # 'origins': zip(origins, origin_tours),
        'footer_2': footer_2,
        'footer_3': footer_3,
    }
    if request.user_agent.is_mobile:
        return render(request, 'ui/mobile/all-tour.html', context)
    else:
        return render(request, 'ui/all-tour.html', context)

def TourDetail(request,id, Slug):
    items = spacial_destinations.objects.filter(show_homepage=True)
    tours_country_list = get_tours_country_list()
    theme_setting = index_page.objects.get(id=1)
    cities_menu = get_menu_cities()
    characters = string.ascii_letters + string.digits
    trs = ''.join(random.choice(characters) for i in range(8))
    date = datetime.now()
    try:
        tour = Tour.objects.get(Slug=Slug)
    except Tour.DoesNotExist:
        raise Http404
    if tour.viewCount is None:
        tour.viewCount = 0
    tour.viewCount += 1
    tour.save(update_fields=["viewCount"])
    gallery = tour_images.objects.filter(tour=tour)
    date_plans = date_plan.objects.filter(tour=tour).order_by('start_date')
    tipe_plan = TripPlan.objects.filter(tour=tour)
    cities = TourCity.objects.filter(TourName_id=tour.id)
    packages = Package.objects.filter(TourName=tour.id).order_by('DoubleBedPrice', 'DoubleBedPrice_doller')
    related_tour = Tour.objects.filter(Tcity=tour.Tcity, PubTour=True).exclude(pk=tour.id).order_by('-id')[:4]
    related_packages = []
    for i in related_tour:
        related_packages.append(Package.objects.filter(TourName=i).order_by('DoubleBedPrice'))
    related_tour = zip(related_tour, related_packages)
    forms = SearchForm()
    form2 = reservsionCreateForm(request.POST or None, prefix='orderform')
    if request.method == 'POST':
        if form2.is_valid():
            orderform = form2.save(commit=False)
            order_pack = request.POST.get('orderpack')
            pack = Package.objects.get(id=int(order_pack))
            orderform.OrderTour = tour
            orderform.OrderTime = date
            orderform.OrderCode = trs
            orderform.OrderPack = order_pack
            orderform.Orderpackage = pack
            orderform.save()
            data = TourOrder.objects.get(id=orderform.id)
            return redirect('order-info', orderform.id, orderform.OrderCode)
    context = {
        'tours_cities_list': cities_menu,
        'Tour': tour,
        'package': packages,
        'Cities': cities,
        'related_tour': related_tour,
        'date_plans': date_plans,
        'Order': form2,
        'Search': forms,
        'set':theme_setting,
        'gallery': gallery,
        'tour_countries': tours_country_list,
        'tipe_plan': tipe_plan,
        'spacialDest': items,
        'meta_robots': tour.meta_robots
    }
    return render(request, 'ui/detail-tour.html', context)

def AllHotelList(request):
    items = spacial_destinations.objects.filter(show_homepage=True)
    tours_country_list = get_tours_country_list()
    view = viewCounter.objects.get(id=1)
    view.hotelsView += 1
    view.save()
    allcities = get_all_hotels_cities()
    hotels_country_with_count = get_hotel_countries_hotel_count()
    all_faqs = faq_home.objects.all()
    theme_setting = index_page.objects.get(id=1)
    countries_hotel = Country.objects.all()
    formsub = SubscribeForm()
    if request.method == 'POST':
        formsub = SubscribeForm(request.POST)
        if formsub.is_valid():
            formsub.save()
            return redirect('/')
    meta_robots = 'INDEX,FOLLOW'

    context = {
        'Sub': formsub,
        'HotelMenu': allcities,
        'countries': hotels_country_with_count,
        'all_faqs': all_faqs,
        'set': theme_setting,
        'tour_countries': tours_country_list,
        'spacialDest': items,
        'countries_hotel': countries_hotel,
        'meta_robots': meta_robots
    }
    return render(request, 'ui/all-hotel.html', context)

def AllCountryHotel(request,id, slug):
    items = spacial_destinations.objects.filter(show_homepage=True)
    tours_country_list = get_tours_country_list()
    reseller_menu = get_top_pages()
    cities_menu = get_menu_cities()
    footer_2 = get_colm_two_pages()
    footer_3 = get_colm_tree_pages()
    theme_setting = index_page.objects.get(id=1)
    try:
        hotelmenu = Country.objects.get(slug=slug)
    except City.DoesNotExist:
        raise Http404
    hotels = get_all_country_hotels(hotelmenu.id)
    all_faqs = hotel_faq_Country.objects.filter(Countryfaq=hotelmenu)
    paginator = Paginator(hotels, 12)
    PageNumber = request.GET.get('page')
    hotels = paginator.get_page(PageNumber)
    cities_hotels_number = get_hotel_cities_hotel_count(hotelmenu.id)
    formsub = SubscribeForm()
    if request.method == 'POST':
        formsub = SubscribeForm(request.POST)
        if formsub.is_valid():
            formsub.save()
            return redirect('/')

    if PageNumber and int(PageNumber) > 1:
        meta_robots = 'NOINDEX,FOLLOW'
    else:
        meta_robots = hotelmenu.hotel_meta_robots

    context = {
        'reseller_menu': reseller_menu,
        'tours_cities_list': cities_menu,
        'Hotels': hotels,
        'country': hotelmenu,
        'all_faqs': all_faqs,
        'set': theme_setting,
        'cities': cities_hotels_number,
        'footer_2': footer_2,
        'footer_3': footer_3,
        'tour_countries': tours_country_list,
        'spacialDest': items,
        "type": "country",
        'meta_robots': meta_robots
    }
    return render(request, 'ui/all-hotel-list.html', context)

def AllHotelCity(request, id, slug):
    items = spacial_destinations.objects.filter(show_homepage=True)
    tours_country_list = get_tours_country_list()
    footer_2 = get_colm_two_pages()
    footer_3 = get_colm_tree_pages()
    theme_setting = index_page.objects.get(id=1)
    try:
        hotelmenu = City.objects.get(slug=slug)
    except City.DoesNotExist:
        raise Http404
    all_faqs = hotel_faq_city.objects.filter(Cityfaq=hotelmenu)    
    meta_robots = hotelmenu.hotel_meta_robots

    context = {
        'city': hotelmenu,
        'all_faqs': all_faqs,
        'set': theme_setting,
        'footer_2': footer_2,
        'footer_3': footer_3,
        'tour_countries': tours_country_list,
        'spacialDest': items,
        'type': 'city',
        'meta_robots': meta_robots
    }
    return render(request, 'ui/all-hotel-list.html', context)

def hotel_search(request):
    items = spacial_destinations.objects.filter(show_homepage=True)
    tours_country_list = get_tours_country_list()
    all_faqs = faq_home.objects.all()
    theme_setting = index_page.objects.get(id=1)
    hotels = Hotel_Data.objects.all().order_by('-id')
    hotel_name = request.GET.get('hotelname')
    hotel_name_en = request.GET.get('hotelnameen')
    hotel_country = request.GET.get('countryname')
    hotel_city = request.GET.get('cityname')
    hotel_rate = request.GET.get('rating')
    if hotel_country:
        item = Country.objects.get(id=int(hotel_country))
        hotels = hotels.filter(Hcountry=item.id)
    if hotel_city:
        item = City.objects.get(id=int(hotel_city))
        hotels = hotels.filter(Hcity=item.id)
    if hotel_name:
        hotels = hotels.filter(HotelName__contains=hotel_name)
    if hotel_name_en:
        hotels = hotels.filter(HotelNameEnglish__contains=hotel_name_en)
    if hotel_rate:
        hotels = hotels.filter(HotelRating=hotel_rate)
    paginator = Paginator(hotels, 12)
    PageNumber = request.GET.get('page')
    hotels = paginator.get_page(PageNumber)
    formsub = SubscribeForm()
    if request.method == 'POST':
        formsub = SubscribeForm(request.POST)
        if formsub.is_valid():
            formsub.save()
            return redirect('/')
    context = {
        'hotels': hotels,
        'Sub': formsub,
        'all_faqs': all_faqs,
        'set': theme_setting,
        'tour_countries': tours_country_list,
        'spacialDest': items
    }
    return render(request, 'ui/hotel_search.html', context)

def HotelDetail(request,id,  Slug):
    items = spacial_destinations.objects.filter(show_homepage=True)
    tours_country_list = get_tours_country_list()
    footer_2 = get_colm_two_pages()
    footer_3 = get_colm_tree_pages()
    theme_setting = index_page.objects.get(id=1)
    try:
        hotel = Hotel_Data.objects.get(Slug=Slug)
    except Hotel_Data.DoesNotExist:
        raise Http404
    gallery = hotel_images.objects.filter(hotel=hotel)
    packages = []
    hp1 = Package.objects.filter(HotelName=hotel, TourName__PubTour=True)
    if hp1.count() > 0:
        for i in hp1:
            packages.append(i)
    hp2 = Package.objects.filter(Mhotel=hotel, TourName__PubTour=True)
    if hp2.count() > 0:
        for i in hp2:
            packages.append(i)
    hp3 = Package.objects.filter(M1hotel=hotel, TourName__PubTour=True)
    if hp3.count() > 0:
        for i in hp3:
            packages.append(i)
    hp4 = Package.objects.filter(M2hotel=hotel, TourName__PubTour=True)
    if hp4.count() > 0:
        for i in hp4:
            packages.append(i)
    hp5 = Package.objects.filter(M3hotel=hotel, TourName__PubTour=True)
    if hp5.count() > 0:
        for i in hp5:
            packages.append(i)
    packages = list(set(packages))
    hotel.viewCount += 1
    hotel.save()
    all_comments = hotel_comments.objects.filter(hotel=hotel, publish=True).order_by('-id')
    comments_form = hotel_comment_form()
    cordinate = hotel.HotelMap.split(',')
    if request.method == 'POST':
        if 'submit_comment' in request.POST:
            comments_form = hotel_comment_form(request.POST)
            hotel_rate = request.POST.get('cmt_rate')
            hotel_rate_mobile = request.POST.get('ct-rate-select')
            if comments_form.is_valid():
                forms = comments_form.save(commit=False)
                forms.hotel = hotel
                forms.create_date = datetime.now()
                if hotel_rate:
                    forms.hotel_rate = hotel_rate
                if hotel_rate_mobile:
                    forms.hotel_rate = hotel_rate_mobile
                forms.save()
                message = 'کامنت شما با موفقیت ارسال شد.'
                messages.success(request, message)
                return redirect('hotel-detail', hotel.id, hotel.Slug)
    context = {
        'HotelData': hotel,
        'set':theme_setting,
        'footer_2': footer_2,
        'footer_3': footer_3,
        'gallery': gallery,
        'packages': packages[:4],
        'tour_countries': tours_country_list,
        'spacialDest': items,
        'comments_form': comments_form,
        'all_comments': all_comments,
        'Lcordinate':cordinate[0],
        'Acordinate':cordinate[1],
        'meta_robots': hotel.meta_robots
    }
    return render(request, 'ui/hotel-detail.html', context)

def TourSearch(request):
    items = spacial_destinations.objects.filter(show_homepage=True)
    tours_country_list = get_tours_country_list()
    select_countries =  Country.objects.all()
    country = request.POST.get('country_id')
    pubTours = get_all_pub_tours()
    cities = City.objects.all()
    packages = Package.objects.all()
    if country:
        country = int(country)
        pubTours = pubTours.filter(Tcountry=country)
        for i in pubTours:
            packages.filter(TourName=i).order_by('-DoubleBedPrice')
        cities = City.objects.filter(CountryName=country)
    city = request.POST.get('city_id')
    if city :
        city = int(city)
        pubTours = pubTours.filter(Tcity=city)
        for i in pubTours:
            packages.filter(TourName=i).order_by('-DoubleBedPrice')
    day = request.POST.get('day_count')
    if day:
        day = int(day)
        pubTours = pubTours.filter(DayCount=day)
        for i in pubTours:
            packages.filter(TourName=i).order_by('-DoubleBedPrice')
    alldata = zip(pubTours, packages)
    footer_2 = get_colm_two_pages()
    footer_3 = get_colm_tree_pages()
    theme_setting = index_page.objects.get(id=1)
    context = {
        'set':theme_setting,
        'footer_2': footer_2,
        'footer_3': footer_3,
        'country': country,
        'city': city,
        'day': day,
        'select_countries': select_countries,
        'cities': cities,
        'pubTours': alldata,
        'tour_countries': tours_country_list,
        'spacialDest': items
    }
    return render(request, 'ui/search-resualt.html', context)

def BlogPage(request):
    items = spacial_destinations.objects.filter(show_homepage=True)
    visa_post = blogPosts.objects.get(id=16)
    tours_country_list = get_tours_country_list()
    theme_setting = index_page.objects.get(id=1)
    view = viewCounter.objects.get(id=1)
    view.blogView += 1
    view.save()
    posts = blogPosts.objects.filter(Publish=True).only('Title', 'Category', 'Image').order_by('-PubDate')[:6]
    all_posts = blogPosts.objects.filter(Publish=True).only('Title', 'Category', 'Image').order_by('-PubDate')
    fav_posts = blogPosts.objects.filter(Publish=True).only('Title', 'Category', 'Image').order_by('-viewCount')[:6]
    if 'post_name' in request.GET:
        post_name = request.GET['post_name']
        if post_name:
            posts = blogPosts.objects.filter(Publish=True, Title__icontains=post_name)
    categories = PostCategory.objects.all()
    ch_categories = PostCategory.objects.exclude(parentCat=None)
    ch_cat_number = []
    for i in categories:
        ch_cat_number.append(PostCategory.objects.filter(parentCat=i).count())
    parent_categories = zip(categories, ch_cat_number)
    paginator = Paginator(all_posts, 10)
    pagenumber = request.GET.get('page')
    data = paginator.get_page(pagenumber)
    
    if pagenumber and int(pagenumber) > 1:
        meta_robots = 'NOINDEX,FOLLOW'
    else:
        meta_robots = 'INDEX,FOLLOW'

    context = {
        'AllCat': categories,
        'Posts': posts,
        'fav_posts': fav_posts,
        'data': data,
        'set': theme_setting,
        'categories': parent_categories,
        'ch_categories': ch_categories,
        'tour_countries': tours_country_list,
        'spacialDest': items,
        'visa_post': visa_post,
        'meta_robots': meta_robots
    }
    return render(request, 'ui/blog.html', context)

def CategoryPost(request, id, slug):
    items = spacial_destinations.objects.filter(show_homepage=True)
    tours_country_list = get_tours_country_list()
    theme_setting = index_page.objects.get(id=1)
    try:
        category = PostCategory.objects.get(id=id, slug=slug)
    except PostCategory.DoesNotExist:
        raise Http404
    menus = Country.objects.filter(showInMenu=True)
    categories = PostCategory.objects.all()
    ch_categories = PostCategory.objects.exclude(parentCat=None)
    ch_cat_number = []
    for i in categories:
        ch_cat_number.append(PostCategory.objects.filter(parentCat=i).count())
    parent_categories = zip(categories, ch_cat_number)
    subcat = PostCategory.objects.filter(parentCat=category)
    posts = blogPosts.objects.filter(Category=category, Publish=True).order_by('-id')
    data = []
    all_posts = []
    for i in subcat:
        data.append(blogPosts.objects.filter(Category=i, Publish=True).order_by('-id'))
    for i in data:
        for j in i:
            all_posts.append(j)
    for i in posts:
        all_posts.append(i)
    listPost = all_posts
    paginator = Paginator(all_posts, 10)
    pageNumber = request.GET.get('page')
    data = paginator.get_page(pageNumber)
    footer = Footer.objects.all()
    formsub = SubscribeForm()
    if request.method == 'POST':
        formsub = SubscribeForm(request.POST)
        if formsub.is_valid():
            formsub.save()
            return redirect('/')
        
    if pageNumber and int(pageNumber) > 1:
        meta_robots = 'NOINDEX,FOLLOW'
    else:
        meta_robots = 'INDEX,FOLLOW'

    context = {
        'Posts': listPost,
        'Footer': footer,
        'Sub': formsub,
        'Menus': menus,
        'set': theme_setting,
        'categories': parent_categories,
        'ch_categories': ch_categories,
        'data':data,
        'tour_countries': tours_country_list,
        'category': category,
        'spacialDest': items,
        'meta_robots': meta_robots
    }
    return render(request, 'post/cartegory-post.html', context)

def PostDetail(request, id, slug):
    items = spacial_destinations.objects.filter(show_homepage=True)
    tours_country_list = get_tours_country_list()
    tset = index_page.objects.get(id=1)
    try:
        post = blogPosts.objects.get(id=id, slug=slug)
    except blogPosts.DoesNotExist:
        raise Http404
    blogPosts.objects.filter(id=post.id).update(viewCount=M.F("viewCount") + 1)
    categories = PostCategory.objects.all()
    ch_categories = PostCategory.objects.exclude(parentCat=None)
    ch_cat_number = []
    for i in categories:
        ch_cat_number.append(PostCategory.objects.filter(parentCat=i).count())
    post_related = related_posts.objects.filter(post=post).order_by('-id')
    fav_post = blogPosts.objects.all().order_by('-viewCount')[:12]
    all_comments = comments.objects.filter(
    post=post,
    publish=True
        ).order_by('-id')
    all_comments_reply = reply_comments.objects.filter(
        publish=True,
        comment__post=post
      ).order_by('-id')
    paginator = Paginator(all_comments, 20)
    pagenumber = request.GET.get('page')
    all_comments = paginator.get_page(pagenumber)
    parent_categories = zip(categories, ch_cat_number)
    context = {
        'fav_posts': fav_post,
        'Post': post,
        'Posts': post_related,
        'all_comments': all_comments,
        'all_comments_reply': all_comments_reply,
        'set': tset,
        'categories': parent_categories,
        'ch_categories': ch_categories,
        'tour_countries': tours_country_list,
        'spacialDest': items,
        'meta_robots': post.meta_robots
    }
    return render(request, 'ui/post-detail.html', context)

def AboutUsUi(request):
    items = spacial_destinations.objects.filter(show_homepage=True)
    tours_country_list = get_tours_country_list()
    footer_2 = get_colm_two_pages()
    footer_3 = get_colm_tree_pages()
    cities_menu = get_menu_cities()
    orgin_menu_cities = get_origin_menu_cities(69)
    theme_setting = index_page.objects.get(id=1)
    view = viewCounter.objects.get(id=1)
    view.aboutView += 1
    view.save()
    about = AboutUs.objects.all()
    context = {
        'tours_cities_list': cities_menu,
        'orgin_menu_cities': orgin_menu_cities,
        'Text': about,
        'set':theme_setting,
        'footer_2': footer_2,
        'footer_3': footer_3,
        'tour_countries': tours_country_list,
        'spacialDest': items
    }
    return render(request, 'ui/about-us.html', context)

def ContactUsUi(request):
    items = spacial_destinations.objects.filter(show_homepage=True)
    tours_country_list = get_tours_country_list()
    theme_setting = index_page.objects.get(id=1)
    view = viewCounter.objects.get(id=1)
    view.contacView += 1
    view.save()
    menulist = Country.objects.filter(showInMenu=True)
    text = ContactUsText.objects.all()
    hotels = Hotel_Data.objects.all()
    hotelcities = []
    for i in hotels:
        hotelcities.append(City.objects.filter(Name=i.Hcity).first())
    hotelcities = City.objects.filter(showInMenu=True)
    hotelcities = list(dict.fromkeys(hotelcities))
    forms = ContactUsForm()
    footer = Footer.objects.all()
    if request.method == 'POST':
        forms = ContactUsForm(request.POST)
        if forms.is_valid():
            forms.save()
            messages.success(request, 'پیام شما با موفقیت ارسال شد')
            return redirect('contact-us')
        else:
            messages.success(request, 'متاسفانه پیام شما ارسال نشد. لطفا مجددا تلاش کنید.')
            return redirect('contact-us')
    formsub = SubscribeForm()
    if request.method == 'POST':
        formsub = SubscribeForm(request.POST)
        if formsub.is_valid():
            formsub.save()
            return redirect('/')
    context = {
        'set':theme_setting,
        'form': forms,
        'Text': text,
        'Footer': footer,
        'Sub': formsub,
        'Menus': menulist,
        'hmenu': hotelcities,
        'tour_countries': tours_country_list,
        'spacialDest': items,
        'meta_robots': 'INDEX,FOLLOW'
    }
    return render(request, 'ui/contact-us.html', context)

def SubscribeFooter(request):
    forms = SubscribeForm()
    if request.method == 'POST':
        forms = SubscribeForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('/')
    context = {
        'Sub': forms
    }
    return render(request, 'ui/footer.html', context)

def orderView(request):
    menulist = Country.objects.filter(showInMenu=True)
    footer = Footer.objects.all()
    hotels = Hotel_Data.objects.all()
    hotelcities = []
    for i in hotels:
        hotelcities.append(City.objects.get(Name=i.Hcity))
    hotelcities = City.objects.filter(showInMenu=True)
    hotelcities = list(dict.fromkeys(hotelcities))
    forms = SearchForm()
    posts = blogPosts.objects.all()
    phone = '09125124784'
    order = TourOrder.objects.filter(Mobile=phone)
    formsub = SubscribeForm()
    if request.method == 'POST':
        formsub = SubscribeForm(request.POST)
        if formsub.is_valid():
            formsub.save()
            return redirect('/')
    context = {'Footer': footer, 'Search': forms, 'Posts': posts, 'Sub': formsub, 'order': order, 'Menus': menulist,
        'hmenu': hotelcities}
    return render(request, 'ui/order.html', context)

def orderInfo(request, id, OrderCode):
    footer_2 = get_colm_two_pages()
    footer_3 = get_colm_tree_pages()
    orgin_menu_cities = get_origin_menu_cities(69)
    cities_menu = get_menu_cities()
    theme_setting = index_page.objects.get(id=1)
    order = TourOrder.objects.get(id=id)
    formsub = SubscribeForm()
    if request.method == 'POST':
        formsub = SubscribeForm(request.POST)
        if formsub.is_valid():
            formsub.save()
            return redirect('/')
    footer = Footer.objects.all()
    menulist = Country.objects.filter(showInMenu=True)
    hotelcities = City.objects.filter(showInMenu=True)
    context = {'Order': order, 'Sub': formsub, 'footer_2': footer_2,
        'footer_3': footer_3, 'tours_cities_list': cities_menu,
        'orgin_menu_cities': orgin_menu_cities,
        'set':theme_setting,'Menus': menulist, 'hmenu': hotelcities}
    return render(request, 'ui/order-info.html', context)

def singleOrderView(request, id, OrderCode):
    order = TourOrder.objects.get(id=id)
    footer = Footer.objects.all()
    menulist = Country.objects.filter(showInMenu=True)
    hotelcities = City.objects.filter(showInMenu=True)
    formsub = SubscribeForm()
    if request.method == 'POST':
        formsub = SubscribeForm(request.POST)
        if formsub.is_valid():
            formsub.save()
            return redirect('/')
    formdoc = createOrderDoc()
    if request.method == 'POST':
        formdoc = createOrderDoc(request.POST, request.FILES)
        if formdoc.is_valid():
            doc = formdoc.save(commit=False)
            doc.ordernum = order
            doc.save()
            emptyform = createOrderDoc()
            message = 'مدارک با موفقیت بارگذاری شد'
            context = {
                'Order': order,
                'Sub': formsub,
                'Footer': footer,
                'Menus': menulist,
                'hmenu': hotelcities,
                'upload': emptyform,
                'msg': message
            }
            return render(request, 'ui/order-view.html', context)
    context = {
        'Order': order,
        'Sub': formsub,
        'Footer': footer,
        'Menus': menulist,
        'hmenu': hotelcities,
        'upload': formdoc
    }
    return render(request, 'ui/order-view.html', context)

def OrderTrack(request):
    usermobile = ''
    usertrs = ''
    formsub = SubscribeForm()
    if request.method == 'POST':
        formsub = SubscribeForm(request.POST)
        if formsub.is_valid():
            formsub.save()
            return redirect('/')
    footer = Footer.objects.all()
    menulist = Country.objects.filter(showInMenu=True)
    hotelcities = City.objects.filter(showInMenu=True)
    if 'usermobile' in request.GET:
        usermobile = request.GET['usermobile']
        if 'usertrs' in request.GET:
            usertrs = request.GET['usertrs']
            order = TourOrder.objects.filter(Mobile=usermobile, OrderCode=usertrs)
            if order:
                return redirect('order-view', order[0].id, order[0].OrderCode)
            else:
                message = 'کاربر عزیز توری با این مشخصات ثبت نگردیده است'
                context = {
                    'Sub': formsub,
                    'Footer': footer,
                    'Menus': menulist,
                    'hmenu': hotelcities,
                    'Msg': message
                }
                return render(request, 'ui/order-search.html', context)
    else:
        context = {
            'Sub': formsub,
            'Footer': footer,
            'Menus': menulist,
            'hmenu': hotelcities
        }
        return render(request, 'ui/order-search.html', context)

def singleMemoView(request, id):
    items = spacial_destinations.objects.filter(show_homepage=True)
    tours_country_list = get_tours_country_list()
    memo = PMemories.objects.get(id=id)
    memo.viewCount += 1
    memo.save()
    spacialTours = get_spacial_tours()
    forms2 = SubscribeForm()
    if request.method == 'POST':
        forms = SubscribeForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('/')
    context = {
        'Memo': memo,
        'Sub': forms2,
        'pubTours': spacialTours,
        'tour_countries': tours_country_list,
        'spacialDest': items,
        'meta_robots': memo.meta_robots
    }
    return render(request, 'ui/single-memo.html', context)


def CategoryMemo(request, slug):
    items = spacial_destinations.objects.filter(show_homepage=True)
    tours_country_list = get_tours_country_list()
    theme_setting = index_page.objects.get(id=1)
    try:
        category = MemoryCategory.objects.get(slug=slug)
    except MemoryCategory.DoesNotExist:
        raise Http404
    menus = Country.objects.filter(showInMenu=True)
    categories = MemoryCategory.objects.all()
    ch_categories = MemoryCategory.objects.exclude(parentCat=None)
    ch_cat_number = []
    for i in categories:
        ch_cat_number.append(MemoryCategory.objects.filter(parentCat=i).count())
    parent_categories = zip(categories, ch_cat_number)
    subcat = MemoryCategory.objects.filter(parentCat=category)
    memories = PMemories.objects.filter(category=category, publish=True).order_by('-id')

    data = []
    all_memos = []
    for i in subcat:
        data.append(PMemories.objects.filter(category=i, publish=True).order_by('-id'))
    for i in data:
        for j in i:
            all_memos.append(j)
    for i in memories:
        all_memos.append(i)
    
    listMemo = all_memos
    paginator = Paginator(all_memos, 10)
    pageNumber = request.GET.get('page')
    data = paginator.get_page(pageNumber)
    footer = Footer.objects.all()
    formsub = SubscribeForm()
    if request.method == 'POST':
        formsub = SubscribeForm(request.POST)
        if formsub.is_valid():
            formsub.save()
            return redirect('/')

    if not all_memos:
        meta_robots = 'NOINDEX,FOLLOW'
    elif pageNumber and int(pageNumber) > 1:
        meta_robots = 'NOINDEX,FOLLOW'
    else:
        meta_robots = 'INDEX,FOLLOW'
        
    context = {
        'PMemories': listMemo,
        'Footer': footer,
        'Sub': formsub,
        'Menus': menus,
        'set': theme_setting,
        'categories': parent_categories,
        'ch_categories': ch_categories,
        'data':data,
        'tour_countries': tours_country_list,
        'spacialDest': items,
        'category': category,
        'meta_robots': meta_robots
    }
    return render(request, 'tour/category-memo.html', context)


def handler404(request, *args, **argv):
    return render(request, 'ui/404.html')


@login_required(login_url='otp_login')
def visa_request(request):
    all_prof = profile.objects.all()
    print(len(all_prof))
    prof = profile.objects.get(user=request.user)
    forms = visa_request_form()
    if request.method == 'POST':
        forms = visa_request_form(request.POST, request.FILES)
        if forms.is_valid():
            trs = random.randint(10000, 99999)
            data = forms.save(commit=False)
            data.trs_number = trs
            data.gender = request.POST.get('gender')
            marial_stat = request.POST.get('marial')
            if marial_stat == 'yes':
                data.marial_stat = True
            if marial_stat == 'no':
                data.marial_stat = False
            if request.POST.get('russia') == 'yes':
                data.russia_relative_stat = True
            if request.POST.get('russia') == 'no':
                data.russia_relative_stat = False
            if request.POST.get('highschool') == 'yes':
                data.uni_degree_stat = True
            if request.POST.get('highschool') == 'no':
                data.uni_degree_stat = False
            data.user = request.user
            data.req_stat = 'Submitted'
            data.save()
            return redirect('visa_list')
        else:
            context = {
                'prof': prof,
                'forms': forms,
                'meta_robots':'NOINDEX,FOLLOW'
            }
            return render(request, 'layout/form-2.html', context)
    context = {
        'prof': prof,
        'forms': forms,
        'meta_robots':'NOINDEX,FOLLOW'
    }
    return render(request, 'layout/form-2.html', context)


@login_required(login_url='otp_login')
def thai_visa_request(request):
    all_prof = profile.objects.all()
    prof = profile.objects.get(user=request.user)
    forms = thaiVisaForm()
    if request.method == 'POST':
        forms = thaiVisaForm(request.POST, request.FILES)
        if forms.is_valid():
            trs = random.randint(10000, 99999)
            data = forms.save(commit=False)
            data.trs_number = trs
            male = request.POST.get('gender1')
            female = request.POST.get('gender2')
            if male:
                data.gender = "Male"
            if female:
                data.gender = "Female"
            single = request.POST.get('marial1')
            maried = request.POST.get('marial2')
            if single:
                data.marial_stat = False
            if maried:
                data.marial_stat = True
            owner = request.POST.get('owner1')
            employee = request.POST.get('owner2')
            if owner:
                data.marial_stat = True
            if employee:
                data.marial_stat = False
            tripthai_yes = request.POST.get('tripthai1')
            tripthai_no = request.POST.get('tripthai12')
            if tripthai_yes:
                data.thai_trip = True
            if tripthai_no:
                data.thai_trip = False
            thaiapply_yes = request.POST.get('thaiapply1')
            thaiapply_no = request.POST.get('thaiapply2')
            if thaiapply_yes:
                data.thai_applied = True
            if thaiapply_no:
                data.thai_applied = False
            data.user = request.user
            data.req_stat = 'Submitted'
            data.save()
            return redirect('thai_visa_list')
        else:
            context = {
                'prof': prof,
                'forms': forms
            }
            return render(request, 'layout/form-thai.html', context)
    context = {
        'prof': prof,
        'forms': forms
    }
    return render(request, 'layout/form-thai.html', context)


def add_reply(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')
        commnet = data.get('comment')
        parent_cm = comments.objects.get(id=int(commnet))
        item = reply_comments.objects.create(full_name=name, email=email, desc=message, comment=parent_cm)
        return JsonResponse({
            'status': '200'
        })

def submitCm(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        email = data.get('email')
        message = data.get('desc')
        postId = data.get('postId')
        post = blogPosts.objects.get(id=int(postId))
        item = comments.objects.create(full_name=name, email=email, desc=message, post=post)
        return JsonResponse({
            'status': '200'
        })

def submitHotelCm(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        email = data.get('email')
        message = data.get('desc')
        hotelId = data.get('hotelId')
        star_rate = data.get('rate')
        hotel = Hotel_Data.objects.get(id=int(hotelId))
        item = hotel_comments.objects.create(full_name=name, email=email, desc=message,
        hotel=hotel, hotel_rate=star_rate)
        return JsonResponse({
            'status': '200'
        })
    
def russia_visa(request):
    item = blogPosts.objects.get(id=16)
    items = spacial_destinations.objects.filter(show_homepage=True)
    theme_setting = index_page.objects.get(id=1)
    top_menu = TourMenu.objects.filter(show_meu=True)
    tours_country_list = get_tours_country_list()

    hotels = Hotel_Data.objects.filter(HotelFeature=True)[:5]
    menulist = Country.objects.filter(showInMenu=True)
    context = {
        'Post': item,
        'Hotels': hotels,
        'Menus': menulist,
        'spacialDest': items,
        'top_menu': top_menu,
        'tour_countries': tours_country_list,
        'set': theme_setting,
    }
    return render(request, 'ui/russia_visa.html', context)