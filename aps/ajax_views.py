import itertools
import json
from datetime import datetime

from django.core.paginator import Paginator
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect

from tour.dataset import *
from tour.models import *

def get_country_tours_city(request):
    country_id = request.GET.get('country_id')
    country = Country.objects.get(id=country_id)
    tours_cities = related_tour_city.objects.filter(tour__PubTour=True, country=country).order_by('city').distinct()
    cities = []
    for i in tours_cities:
        cities.append(i.city)
    cities = list(set(cities))
    context={
        'country': country,
        'tours_cities': cities
    }
    return render(request, 'ui/ajax_tours_cities.html', context)

def get_country_tours_city_mobile(request):
    country_id = request.GET.get('country_id')
    country = Country.objects.get(id=country_id)
    tours_cities = City.objects.filter(tour_city__isnull=False, CountryName=country).order_by('tour_city').distinct()
    context={
        'country': country,
        'tours_cities': tours_cities
    }
    return render(request, 'ui/offcanvas-tour-cities.html', context)

def index_posts_list(request):
    posts = blogPosts.objects.filter(Publish=True).order_by('-PubDate')
    context = {
        'Posts': posts
    }
    return render(request, 'ajax/index_post_list.html', context)

def ajax_tour_list(request):
    tours = Tour.objects.filter(PubTour=True).order_by('-id')
    packages = Package.objects.filter(TourName__in=tours).order_by('-DoubleBedPrice')
    cities = TourCity.objects.filter(TourName__in=tours)
    tours_paginator = Paginator(tours, 10)
    tours_page = request.GET.get('page')
    tours = tours_paginator.get_page(tours_page)
    cities_paginator = Paginator(cities, 10)
    cities_page = request.GET.get('page')
    cities = cities_paginator.get_page(cities_page)
    packages_paginator = Paginator(packages, 10)
    packages_page = request.GET.get('page')
    packages = packages_paginator.get_page(packages_page)
    alldata = zip(tours, cities, packages)
    context = {
        'AllTour': tours,
        'AllData' : alldata
    }
    return render(request, 'ajax/tour_list.html', context)

def index_tours_ajax(request):
    if request.method == 'POST':
        pubTours = get_all_pub_tours()
        packages = get_tours_packages_data()
        cities = get_tours_cities_data()
        data = zip(pubTours, packages, cities)
        context = {
            'pubTours': data
        }
        return render(request, 'ajax/layout/spacial_tour_list.html', context)
    else:
        return JsonResponse({
            'Developer': 'Soroush Khani',
            'Mobile Number': '0912 512 4784'
        })

def index_posts_ajax(request):
    if request.method == 'POST':
        posts = get_all_pub_posts()
        visa_post = blogPosts.objects.get(id=16)
        context = {
            'Posts':posts,
            'visa_post': visa_post
        }
        return render(request, 'ajax/layout/post_list.html', context)
    else:
        return JsonResponse({
            'Developer': 'Soroush Khani',
            'Mobile Number': '0912 512 4784'
        })

def list_tours_ajax(request):
    pubTours = get_all_pub_tours()
    packages = get_tours_packages_data()
    cities = get_tours_cities_data()
    paginator = Paginator(pubTours, 9)
    pagenumber = request.GET.get('page')
    pubTours = paginator.get_page(pagenumber)
    paginator2 = Paginator(packages, 9)
    pagenumber2 = request.GET.get('page')
    packages = paginator2.get_page(pagenumber2)
    paginator3 = Paginator(cities, 9)
    pagenumber3 = request.GET.get('page')
    cities = paginator3.get_page(pagenumber3)
    data = zip(pubTours, packages, cities)
    context = {
        'pubTours':data,
        'tours_list': pubTours
    }
    return render(request, 'ajax/layout/spacial_tour_list.html', context)

def list_tours_ajax_horzental(request):
    pubTours = get_all_pub_tours()
    packages = get_tours_packages_data()
    cities = get_tours_cities_data()
    dates = []
    for tour in pubTours:
        tour_dates = date_plan.objects.filter(tour=tour).count()
        dates.append(tour_dates)
    paginator = Paginator(pubTours, 9)
    pagenumber = request.GET.get('page')
    pubTours = paginator.get_page(pagenumber)
    paginator2 = Paginator(packages, 9)
    pagenumber2 = request.GET.get('page')
    packages = paginator2.get_page(pagenumber2)
    paginator3 = Paginator(cities, 9)
    pagenumber3 = request.GET.get('page')
    cities = paginator3.get_page(pagenumber3)
    paginator4 = Paginator(dates, 9)
    pagenumber4 = request.GET.get('page')
    dates = paginator4.get_page(pagenumber4)
    data = zip(pubTours, packages, cities, dates)
    context = {
        'pubTours':data,
        'tours_list': pubTours
    }
    return render(request, 'ajax/layout/tour-list.html', context)

def list_tours_ajax_menu_horzental(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        menu_slug = data.get('menu')
        menu = TourMenu.objects.get(slug=menu_slug)
        tourlist = Tour.objects.filter(TourMenu=menu.id, PubTour=True).only('Title', 'NightCount', 'DayCount', 'Cash', 'Installment').order_by('-updateDate')
        date = datetime.now()
        date = date.date()
        ArchiveTour = Tour.objects.filter(TourMenu=menu.id, StartDate=date)
        for tour in ArchiveTour:
            tour.PubTour = False
            tour.save()
        cities = []
        for i in tourlist:
            cities.append(TourCity.objects.filter(TourName_id=i))
        paginator = Paginator(tourlist, 10)
        PageNumber = request.GET.get('page')
        tourlist = paginator.get_page(PageNumber)
        packages = []
        for i in tourlist:
            packages.append(Package.objects.filter(TourName_id=i.id).order_by('DoubleBedPrice'))
        dates = []
        for tour in tourlist:
            tour_dates = date_plan.objects.filter(tour=tour).count()
            dates.append(tour_dates)
        paginator = Paginator(tourlist, 9)
        pagenumber = request.GET.get('page')
        pubTours = paginator.get_page(pagenumber)
        paginator2 = Paginator(packages, 9)
        pagenumber2 = request.GET.get('page')
        packages = paginator2.get_page(pagenumber2)
        paginator3 = Paginator(cities, 9)
        pagenumber3 = request.GET.get('page')
        cities = paginator3.get_page(pagenumber3)
        paginator4 = Paginator(dates, 9)
        pagenumber4 = request.GET.get('page')
        dates = paginator4.get_page(pagenumber4)
        data = zip(pubTours, packages, cities, dates)
        context = {
            'pubTours':data,
            'tours_list': pubTours
        }
        return render(request, 'ajax/layout/tour-list.html', context)
    else:
        return JsonResponse({
            'Developer': 'Soroush Khani',
            'Mobile Number': '0912 512 4784'
        })
def country_tours_ajax(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        country = data.get('country')
        try:
            menu = Country.objects.get(slug=country)
        except Country.DoesNotExist:
            raise Http404
        tourlist = get_country_tours(menu.id)
        packages = get_country_tours_packages(menu.id)
        cities = get_country_tours_cities(menu.id)
        dates = []
        for tour in tourlist:
            tour_dates = date_plan.objects.filter(tour=tour).count()
            dates.append(tour_dates)
        paginator = Paginator(tourlist, 9)
        PageNumber = data.get('page')
        tourlist = paginator.get_page(PageNumber)
        paginator2 = Paginator(cities, 9)
        PageNumber2 = data.get('page')
        cities = paginator2.get_page(PageNumber2)
        paginator3 = Paginator(packages, 9)
        PageNumber3 = data.get('page')
        packages = paginator3.get_page(PageNumber3)
        alldata = zip(tourlist, packages, cities, dates)
        context = {
            'pubTours':alldata,
            'tours_list': tourlist
        }
        return render(request, 'ajax/layout/tour-list.html', context)
    else:
        return JsonResponse({
            'Developer': 'Soroush Khani',
            'Mobile Number': '0912 512 4784'
        })

def city_tours_ajax(request):
    if request.method == "POST":
        data = json.loads(request.body)
        city = data.get('city')
        try:
            menu = City.objects.get(slug=city)
        except Country.DoesNotExist:
            raise Http404
        tourlist = get_city_tours(menu.id)
        packages = get_city_tours_packages(menu.id)
        cities = get_city_tours_cities(menu.id)
        dates = []
        for tour in tourlist:
            tour_dates = date_plan.objects.filter(tour=tour).count()
            dates.append(tour_dates)
        paginator = Paginator(tourlist, 9)
        PageNumber = data.get('page')
        tourlist = paginator.get_page(PageNumber)
        paginator2 = Paginator(cities, 9)
        PageNumber2 = data.get('page')
        cities = paginator2.get_page(PageNumber2)
        paginator3 = Paginator(packages, 9)
        PageNumber3 = data.get('page')
        packages = paginator3.get_page(PageNumber3)
        alldata = zip(tourlist, packages, cities,dates)
        context = {
            'pubTours':alldata,
            'tours_list': tourlist
        }
        return render(request, 'ajax/layout/tour-list.html', context)
    else:
        return JsonResponse({
            'Developer': 'Soroush Khani',
            'Mobile Number': '0912 512 4784'
        })

def hotel_cities_ajax(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        allcities = get_all_hotels_cities()
        paginator = Paginator(allcities, 12)
        pagenumber = data.get('page')
        allcities = paginator.get_page(pagenumber)
        context = {
            'hotels': allcities
        }
        return render(request, 'ajax/hotel-list.html', context)
    else:
        return JsonResponse({
            'Developer': 'Soroush Khani',
            'Mobile Number': '0912 512 4784'
        })

def country_hotels_ajax(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        country_slug = data.get('country')
        country = Country.objects.get(slug=country_slug)
        allcountries = get_all_country_hotels(country.id)
        paginator = Paginator(allcountries, 12)
        pagenumber = data.get('page')
        allcountries = paginator.get_page(pagenumber)
        context = {
            'hotels': allcountries
        }
        return render(request, 'ajax/country-hotel-list.html', context)
    else:
        return JsonResponse({
            'Developer': 'Soroush Khani',
            'Mobile Number': '0912 512 4784'
        })

def city_hotels_ajax(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        city_slug = data.get('city')
        city = City.objects.get(slug=city_slug)
        allcities = get_all_city_hotels(city.id)
        paginator = Paginator(allcities, 12)
        pagenumber = data.get('page')
        allcities = paginator.get_page(pagenumber)
        context = {
            'hotels': allcities
        }
        return render(request, 'ajax/country-hotel-list.html', context)
    else:
        return JsonResponse({
            'Developer': 'Soroush Khani',
            'Mobile Number': '0912 512 4784'
        })

def get_country_city(request):
    country = request.GET.get('country_id')
    cities = City.objects.filter(CountryName=country)
    context = {
        'cities': cities
    }
    return render(request, 'ajax/layout/country-city.html', context)

def sidebar_filter(request):
    fromPrice = request.GET.get('fromPrice')
    toPrice = request.GET.get('toPrice')
    dayCount = request.GET.get('dayCount')
    country = request.GET.get('selectedCountry', '[]')
    country = json.loads(country)
    city = request.GET.get('selectedCity', '[]')
    city = json.loads(city)
    hotelRate = request.GET.get('hotelRate', '[]')
    hotelRate = json.loads(hotelRate)
    airlines = request.GET.get('airlines', '[]')
    airlines = json.loads(airlines)
    all_packages = get_tours_packages_data()
    all_tours = get_all_pub_tours()
    packages_list = []
    packages = []
    tours_list = []
    cities = []
    for i in all_packages:
        for j in i:
            packages_list.append(j)
    if country:
        for i in country:
            new_list = all_tours.filter(Tcountry=i, DayCount__contains=dayCount)
            for j in new_list:
                tours_list.append(j)
            if city:
                tours_list = []
                for i in city:
                    new_list = all_tours.filter(Tcity=i, DayCount__contains=dayCount)
                    for j in new_list:
                        tours_list.append(j)
    if city:
        tours_list = []
        for i in city:
            new_list = all_tours.filter(Tcity=i, DayCount__contains=dayCount)
            for j in new_list:
                tours_list.append(j)
    if not country and not city:
        tours_list = all_tours.filter(DayCount__contains=dayCount)
    if airlines:
        new_t_list_2 = []
        for i in airlines:
            for j in tours_list:
                airline_city = TourCity.objects.filter(TourName=j).first()
                if airline_city.Airline and airline_city.Airline.id == int(i):
                    new_t_list_2.append(j)
                    cities.append(airline_city)
        new_t_list_2 = list(set(new_t_list_2))
        tours_list = new_t_list_2

    if not country and not city and not airlines:
        tours_list = all_tours.filter(DayCount__contains=dayCount)
    for j in tours_list:
        cities.append(TourCity.objects.filter(TourName=j).first())
    for i in tours_list:
        packages.append(
            Package.objects.filter(TourName=i, DoubleBedPrice__gte=fromPrice, DoubleBedPrice__lte=toPrice).order_by(
                'DoubleBedPrice'))
    if hotelRate:
        new_t_list = []
        for i in hotelRate:
            for j in packages:
                for k in j:
                    if k.HotelName:
                        hotel = k.HotelName
                        if hotel.HotelRating == i:
                            new_t_list.append(k.TourName)
        new_t_list = list(set(new_t_list))
        tours_list = new_t_list
    price_package = []
    price_tours = []
    for i in packages:
        for j in i:
            if j != None:
                price_package.append(j)
                price_tours.append(j.TourName)
    packages = price_package
    tours = list(set(price_tours))
    pubTours = zip(tours, packages, cities)
    context = {
        'pubTours': pubTours,
        'tours': tours_list,
        'packages': packages,
        'cities': cities
    }
    return render(request, 'ajax/layout/filter-tour-list.html', context)

def sidebar_filter_city(request):
    country = request.GET.get('selectedCountry', '[]')
    country = json.loads(country)
    cities = []
    if country:
        for i in country:
            new_list = Tour.objects.filter(Tcountry=i)
            for j in new_list:
                cities.append(j.Tcity)
    else:
        for i in Tour.objects.all():
            cities.append(i.Tcity)
    cities = list(set(cities))
    context = {
        'cities': cities
    }
    return render(request, 'ajax/layout/sibar-citiy.html', context)

def menuSearch(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        searchTerm = data.get('search')
        if searchTerm != '':
            countries = list(Country.objects.filter(tocountry__PubTour=True, TitleC__icontains=searchTerm).distinct())
            tours_cities = list(City.objects.filter(tour_city__isnull=False, tour_city__PubTour=True, Name__icontains=searchTerm).order_by(
                'tour_city').distinct())
            for i in tours_cities:
                countries.append(i.CountryName)
            countries = list(set(countries))
            context = {
                'search_countries': countries,
                'search_cities': tours_cities
            }
            return render(request, 'ui/base/menu-search.html', context)
        else:
            countries = Country.objects.filter(tocountry__PubTour=True, TitleC__icontains=searchTerm).distinct()
            context = {
                'tour_countries': countries,

            }
            return render(request, 'ui/base/empty-menu-search.html', context)
    else:
        return JsonResponse({
            'Developer': 'Soroush Khani',
            'Mobile': '0912 512 4784'
        })