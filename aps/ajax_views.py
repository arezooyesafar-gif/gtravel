import itertools
import json
from datetime import datetime

from django.core.paginator import Paginator
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect

from tour.dataset import *
from tour.models import *
from tour.date_pricing import compute_tour_min_price, tour_card_packages, tour_card_packages_bulk


def get_country_tours_city(request):
    country_id = request.GET.get('country_id')
    country = Country.objects.get(id=country_id)
    cities = []
    direct_tours = Tour.objects.filter(
        Tcountry=country,
        PubTour=True
    ).select_related('Tcity')
    for tour in direct_tours:
        if tour.Tcity:
            cities.append(tour.Tcity)
    related_items = related_tour_city.objects.filter(
        country=country,
        tour__PubTour=True
    ).select_related('city')
    for item in related_items:
        if item.city:
            cities.append(item.city)

    unique_cities = {}
    for city in cities:
        unique_cities[city.id] = city
    cities = sorted(
        unique_cities.values(),
        key=lambda x: x.Name
    )
    context = {
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

def get_country_hotel_cities(request):
    country_id = request.GET.get('country_id')
    country = Country.objects.get(id=country_id)
    hotel_cities = City.objects.filter(hotel_city__isnull=False, CountryName=country).order_by('Name').distinct()
    context = {
        'country': country,
        'hotel_cities': hotel_cities
    }
    return render(request, 'ui/ajax_hotel_cities.html', context)

def get_country_hotel_cities_mobile(request):
    country_id = request.GET.get('country_id')
    country = Country.objects.get(id=country_id)
    hotel_cities = City.objects.filter(hotel_city__isnull=False, CountryName=country).order_by('Name').distinct()
    context = {
        'country': country,
        'hotel_cities': hotel_cities
    }
    return render(request, 'ui/offcanvas-hotel-cities.html', context)


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
    paginator = Paginator(pubTours, 11)
    pagenumber = request.GET.get('page')
    pubTours = paginator.get_page(pagenumber)
    paginator2 = Paginator(packages, 11)
    pagenumber2 = request.GET.get('page')
    packages = paginator2.get_page(pagenumber2)
    paginator3 = Paginator(cities, 11)
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
        tour_dates = date_plan.objects.filter(tour=tour).exclude(start_date=tour.StartDate).count()
        dates.append(tour_dates)
    paginator = Paginator(pubTours, 11)
    pagenumber = request.GET.get('page')
    pubTours = paginator.get_page(pagenumber)
    paginator2 = Paginator(packages, 11)
    pagenumber2 = request.GET.get('page')
    packages = paginator2.get_page(pagenumber2)
    paginator3 = Paginator(cities, 11)
    pagenumber3 = request.GET.get('page')
    cities = paginator3.get_page(pagenumber3)
    paginator4 = Paginator(dates, 11)
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
        Tour.objects.filter(TourMenu=menu.id, StartDate=date).update(PubTour=False)
        paginator = Paginator(tourlist, 11)
        pagenumber = request.GET.get('page')
        pubTours = paginator.get_page(pagenumber)
        t_ids = [i.id for i in pubTours]
        cits_qs = TourCity.objects.filter(TourName_id__in=t_ids)
        dts_qs = date_plan.objects.filter(tour_id__in=t_ids).values('tour_id').annotate(cnt=M.Count('id'))
        cits_map = {}
        for c in cits_qs:
            cits_map.setdefault(c.TourName_id, []).append(c)
        dts_map = {d['tour_id']: d['cnt'] for d in dts_qs}
        _bulk = tour_card_packages_bulk(list(pubTours))
        packages = [_bulk.get(i.id, []) for i in pubTours]
        cities = [cits_map.get(i.id, []) for i in pubTours]
        dates = [dts_map.get(i.id, 0) for i in pubTours]
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
            tour_dates = date_plan.objects.filter(tour=tour).exclude(start_date=tour.StartDate).count()
            dates.append(tour_dates)
        paginator = Paginator(tourlist, 11)
        PageNumber = data.get('page')
        tourlist = paginator.get_page(PageNumber)
        paginator2 = Paginator(cities, 11)
        PageNumber2 = data.get('page')
        cities = paginator2.get_page(PageNumber2)
        paginator3 = Paginator(packages, 11)
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
            tour_dates = date_plan.objects.filter(tour=tour).exclude(start_date=tour.StartDate).count()
            dates.append(tour_dates)
        paginator = Paginator(tourlist, 11)
        PageNumber = data.get('page')
        tourlist = paginator.get_page(PageNumber)
        paginator2 = Paginator(cities, 11)
        PageNumber2 = data.get('page')
        cities = paginator2.get_page(PageNumber2)
        paginator3 = Paginator(packages, 11)
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
        
def custom_category_tours_ajax(request):
    if request.method == 'POST':

        data = json.loads(request.body)

        slug = data.get('slug')

        category = CustomTourCategory.objects.get(slug=slug)

        tourlist = Tour.objects.filter(
            custom_categories=category,
            PubTour=True
        ).order_by('-id')

        packages = []
        cities = []
        dates = []
        _bulk = tour_card_packages_bulk(list(tourlist))

        for tour in tourlist:

            packages.append(_bulk.get(tour.id, []))

            cities.append(
                TourCity.objects.filter(
                    TourName=tour
                )
            )

            dates.append(
                date_plan.objects.filter(
                    tour=tour
                ).count()
            )

        paginator = Paginator(tourlist, 9)

        page = data.get('page')

        tourlist = paginator.get_page(page)

        paginator2 = Paginator(packages, 9)
        packages = paginator2.get_page(page)

        paginator3 = Paginator(cities, 9)
        cities = paginator3.get_page(page)

        paginator4 = Paginator(dates, 9)
        dates = paginator4.get_page(page)

        pubTours = zip(
            tourlist,
            packages,
            cities,
            dates
        )

        context = {
            'pubTours': pubTours,
            'tours_list': tourlist
        }

        return render(
            request,
            'ajax/layout/tour-list.html',
            context
        )

    return JsonResponse({'error': 'invalid request'})

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
    city_map = {}
    for t in list(tours_list):
        tc = TourCity.objects.filter(TourName=t).first()
        if tc:
            city_map[t.id] = tc
    from tour.models import Footer as _Footer
    _f = _Footer.objects.first()
    _rate = _f.dollar_rate if _f else 170000
    _from = int(fromPrice) if fromPrice else 0
    _to = int(toPrice) if toPrice else 9999999999
    tour_matched = []
    for tour in list(tours_list):
        every_pkg = list(Package.objects.filter(TourName=tour).select_related('Pcry', 'fr_Pcry'))
        if not every_pkg:
            continue
        base_dp = date_plan.objects.filter(tour=tour, start_date=tour.StartDate).first()
        best = compute_tour_min_price(every_pkg, base_dp)
        display_pool = [p for p in every_pkg if not p.exclusive_date_plan_id] or every_pkg
        display_pool.sort(key=lambda p: ((p.DoubleBedPrice or 0), (p.DoubleBedPrice_doller or 0)))
        display_pkg = display_pool[0]
        if best:
            eff_price = best['price'] or 0
            eff_dollar = best['price_dollar'] or 0
        else:
            eff_price = display_pkg.DoubleBedPrice or 0
            eff_dollar = display_pkg.DoubleBedPrice_doller or 0
        if eff_price >= 1000000:
            total = eff_price + eff_dollar * _rate
        else:
            total = eff_price * _rate
        if not (_from <= total <= _to):
            continue
        if best:
            display_pkg.DoubleBedPrice = best['price']
            display_pkg.DoubleBedPrice_doller = best['price_dollar']
            display_pkg.DollerPrice = None
        tour_matched.append((tour, display_pool, display_pkg))
    if hotelRate:
        filtered_tm = []
        for tour, pkgs, display_pkg in tour_matched:
            for pkg in pkgs:
                if pkg.HotelName and pkg.HotelName.HotelRating in [str(r) for r in hotelRate]:
                    filtered_tm.append((tour, pkgs, display_pkg))
                    break
        tour_matched = filtered_tm
    final_tours = [t for t, _, _ in tour_matched]
    final_packages = [display_pkg for _, _, display_pkg in tour_matched]
    final_cities = [city_map.get(t.id) for t in final_tours]
    pubTours = zip(final_tours, final_packages, final_cities)
    context = {
        'pubTours': pubTours,
        'tours': final_tours,
        'packages': final_packages,
        'cities': final_cities
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
def get_tour_dates_ajax(request, tour_id):
    tour = Tour.objects.get(id=tour_id)
    dates = date_plan.objects.filter(tour=tour).exclude(start_date=tour.StartDate).order_by('start_date')
    base_date_plan = date_plan.objects.filter(tour=tour, start_date=tour.StartDate).first()
    all_packages = list(Package.objects.filter(TourName=tour).select_related('Pcry', 'fr_Pcry'))

    base_best = compute_tour_min_price(all_packages, base_date_plan)
    if base_best:
        min_price = base_best['price']
        min_price_dollar = base_best['price_dollar']
        min_currency = base_best['currency']
        min_currency_foreign = base_best['currency_foreign']
    else:
        min_price = 0
        min_price_dollar = 0
        min_currency = 'تومان'
        min_currency_foreign = 'دلار'

    dates_with_price = []
    for d in dates:
        item_best = compute_tour_min_price(all_packages, d)
        fp_toman = item_best['price'] if item_best else min_price
        fp_dollar = item_best['price_dollar'] if item_best else min_price_dollar
        color = 'up' if fp_toman > min_price else 'down' if fp_toman < min_price else 'neutral'
        dates_with_price.append({'date': d, 'final_price': fp_toman, 'final_price_dollar': fp_dollar, 'color': color})
    main_color = 'neutral'
    context = {'dates_with_price': dates_with_price, 'tour': tour, 'min_price': min_price, 'min_price_dollar': min_price_dollar, 'min_currency': min_currency, 'min_currency_foreign': min_currency_foreign, 'main_color': main_color}
    return render(request, 'ajax/tour_dates_popup.html', context)

def save_tour_interest(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name', '').strip()
            family = data.get('family', '').strip()
            phone = data.get('phone', '').strip()
            page_type = data.get('page_type', '').strip()
            page_slug = data.get('page_slug', '').strip()
            if phone:
                TourInterest.objects.create(name=name, family=family, phone=phone, page_type=page_type, page_slug=page_slug)
                return JsonResponse({'status': 'ok'})
            return JsonResponse({'status': 'error', 'msg': 'شماره موبایل الزامی است'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'msg': str(e)}, status=400)
    return JsonResponse({'status': 'error'}, status=405)



