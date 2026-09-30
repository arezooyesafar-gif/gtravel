import json
import random
from html import unescape
import string
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils.html import strip_tags

from django.db import models as M
from django.db.models import Q, Case, When, Value, IntegerField
from hotels.forms import hotel_comment_form
from hotels.models import Hotel_Data, hotel_images, hotel_comments
from person.models import profile
from tour.dataset import *
from tour.date_pricing import (compute_tour_min_price, tour_card_packages,
                               tour_card_packages_bulk, apply_own_base_price_bulk,
                               packages_for_date)
from django.contrib import messages
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from theme.models import index_page
from tour.forms import SearchForm, ContactUsForm, SubscribeForm, reservsionCreateForm, createOrderDoc
from pages.dataset import *
from visa.forms import visa_request_form, thaiVisaForm
from blog.models import *
from django.shortcuts import get_object_or_404, render


def IndexPage(request):
    date = datetime.now()
    date = date.date()
    # ArchiveTour = Tour.objects.filter(StartDate=date)
    # for tour in ArchiveTour:
    #     tour.PubTour = False
    #     tour.save()
    # Tour.objects.filter(StartDate=date).update(PubTour=False)
    theme_setting = index_page.objects.get(id=1)
    view = viewCounter.objects.get(id=1)
    view.indexView += 1
    view.save()

    # These reads are expensive (N+1-prone) but not request-specific, so they're
    # cached at the data level instead of caching the whole rendered page — that
    # way {% csrf_token %} in the search/subscribe forms below is always rendered
    # fresh per-request instead of a stale token getting baked into a cached page.
    # The rollover call below is a write with side effects (not just a read), but
    # it's kept here on purpose: this preserves its exact original once-per-cache-
    # window frequency from when the page itself was cached with @cache_page, and
    # leaves its filter args (including force_pub) completely untouched since
    # their exact intent isn't known here.
    homepage_data = cache.get('homepage_index_data')
    if homepage_data is None:
        roll_over_expired_tour_dates(Tour.objects.filter(StartDate__lte=date, PubTour=True, force_pub=False))
        homepage_data = {
            'items': spacial_destinations.objects.select_related('country', 'city').filter(show_homepage=True),
            'all_faqs': faq_home.objects.all(),
            'countries': get_tours_country(),
            'select_countries': Country.objects.all(),
            'tours_country_list': get_tours_country_list(),
            'spacialTours': get_spacial_tours(),
            'latest_tours': get_all_pub_tours(),
            'latest_packages': get_tours_packages_data(),
            'latest_cities': get_tours_cities_data(),
            'latest_posts': get_all_pub_posts(),
            'top_menu': TourMenu.objects.filter(show_meu=True),
            'visa_post': blogPosts.objects.get(id=16),
        }
        cache.set('homepage_index_data', homepage_data, 60 * 10)

    forms = SearchForm()
    formsub = SubscribeForm()
    if request.method == 'POST':
        formsub = SubscribeForm(request.POST)
        if formsub.is_valid():
            formsub.save()
            return redirect('/')

    latest_tours_data = zip(
        homepage_data['latest_tours'],
        homepage_data['latest_packages'],
        homepage_data['latest_cities'],
    )

    context = {
        'all_faqs': homepage_data['all_faqs'],
        'Search': forms,
        'Sub': formsub,
        'set': theme_setting,
        'countries': homepage_data['countries'],
        'tour_countries': homepage_data['tours_country_list'],
        'SpacialData': homepage_data['spacialTours'],
        'select_countries': homepage_data['select_countries'],
        'spacialDest': homepage_data['items'],
        'top_menu': homepage_data['top_menu'],
        'LatestToursData': latest_tours_data,
        'LatestToursList': homepage_data['latest_tours'],
        'Posts': homepage_data['latest_posts'],
        'visa_post': homepage_data['visa_post'],
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

    # Same reasoning as AllTourList: cache the reads that are the same for every
    # country page (menu/footer/airlines/etc.), not the whole rendered page, so
    # {% csrf_token %} in this template always gets a fresh token instead of a
    # stale one baked into a cached page.
    shared_data = cache.get('category_tour_shared_data')
    if shared_data is None:
        shared_data = {
            'reseller_menu': get_top_pages(),
            'footer_2': get_colm_two_pages(),
            'footer_3': get_colm_tree_pages(),
            'tours_country_list': get_tours_country_list(),
            'airlines': get_airlines(),
            'items': spacial_destinations.objects.select_related('country', 'city').filter(show_homepage=True),
        }
        cache.set('category_tour_shared_data', shared_data, 60 * 10)

    contry_cities = get_contry_cities(menu.id)
    contry_cities_post = contry_cities
    faqs = FAQ.objects.filter(Countryfaq=menu.id)
    forms = SearchForm()
    theme_setting = index_page.objects.get(id=1)
    dest_cities = City.objects.filter(CountryName=menu)
    country_media = CityCountryMedia.objects.filter(country_id=id, is_active=True).order_by('sort_order', '-created_at')
    meta_robots = menu.tour_meta_robots

    tourlist = get_country_tours(menu.id)

    page_number = request.GET.get('page', 1)
    paginator = Paginator(tourlist, 11)
    tourlist = paginator.get_page(page_number)

    packages = []
    tour_cities = []
    dates = []

    # for tour in tourlist:
    #     packages.append(
    #    Package.objects.filter(TourName=tour).order_by('DoubleBedPrice', 'DoubleBedPrice_doller')
    #     )

    #     tour_cities.append(
    #     list(TourCity.objects.filter(TourName=tour).select_related('Airline', 'FromAirport', 'ToAirport'))
    #     )

    #     dates.append(
    #     date_plan.objects.filter(tour=tour).count()
    #    )

    tour_ids = [tour.id for tour in tourlist]

    packages_qs = Package.objects.filter(
        TourName__in=tour_ids, exclusive_date_plan__isnull=True
    ).order_by('DoubleBedPrice', 'DoubleBedPrice_doller')
    cities_qs = list(TourCity.objects.filter(TourName__in=tour_ids).select_related('Airline', 'FromAirport', 'ToAirport'))
    dates_qs = date_plan.objects.filter(tour__in=tour_ids).values('tour_id').annotate(cnt=M.Count('id'))

    packages_map = {}
    for p in packages_qs:
        packages_map.setdefault(p.TourName_id, []).append(p)

    cities_map = {}
    for c in cities_qs:
        cities_map.setdefault(c.TourName_id, []).append(c)

    dates_map = {d['tour_id']: d['cnt'] for d in dates_qs}

    card_packages = tour_card_packages_bulk(list(tourlist))
    for tour in tourlist:
        packages.append(card_packages.get(tour.id, []))
        tour_cities.append(cities_map.get(tour.id, []))
        dates.append(dates_map.get(tour.id, 0))


    alldata = list(zip(tourlist, packages, tour_cities, dates))

    context = {
        'reseller_menu': shared_data['reseller_menu'],
        'Search': forms,
        'all_faqs': faqs,
        'country': menu,
        'set': theme_setting,
        'cities': contry_cities,
        'cities_post': contry_cities_post,
        'footer_2': shared_data['footer_2'],
        'footer_3': shared_data['footer_3'],
        'tour_countries': shared_data['tours_country_list'],
        'dest_cities': dest_cities,
        'airlines': shared_data['airlines'],
        'spacialDest': shared_data['items'],
        'media_list': country_media,
        'meta_robots': meta_robots,
        'pubTours': alldata,
        'tours_list': tourlist,
        # Legacy mobile template compatibility (keep the old mobile UI intact)
        'AllTour': tourlist,
        'AllData': list(zip(tourlist, tour_cities, packages)),
        'contry': menu,
    }
    # تقویم جلالی (django_jalali.js + jquery-ui.min.css) فقط برای فرم‌هایی
    # لازم است که ورودی تاریخ دارند. این صفحه ندارد، ولی ۸۲ کیلوبایت را
    # روی هر بازدید دانلود می‌کرد.
    context['skip_jalali_datepicker'] = True
    # سه نظر مشتریان همین کشور (از پنل ثبت می‌شوند؛ نظرات گوگل مپ قابل
    # خواندن خودکار نیستند - Places API حداکثر ۵ نظرِ غیرقابل‌فیلتر می‌دهد
    # و از ایران هم در دسترس نیست)
    context['tour_reviews'] = list(
        TourReview.objects.filter(publish=True, country=menu)[:3]
    )
    context['memory_category'] = get_country_memory_category(menu)
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
        cities.append(list(TourCity.objects.filter(TourName_id=i).select_related('Airline', 'FromAirport', 'ToAirport')))
    paginator = Paginator(tours, 10)
    PageNumber = request.GET.get('page')
    tours = paginator.get_page(PageNumber)
    packages = []
    card_packages = tour_card_packages_bulk(list(tours))
    for i in tours:
        packages.append(card_packages.get(i.id, []))
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
    # تقویم جلالی (django_jalali.js + jquery-ui.min.css) فقط برای فرم‌هایی
    # لازم است که ورودی تاریخ دارند. این صفحه ندارد، ولی ۸۲ کیلوبایت را
    # روی هر بازدید دانلود می‌کرد.
    context['skip_jalali_datepicker'] = True
    return render(request, 'ui/all-tour.html', context)
def CityTourList(request,slug, id):
    try:
        menu = City.objects.get(slug=slug)
    except City.DoesNotExist:
        raise Http404

    # Same reasoning as CategoryTourList/AllTourList: cache the reads that are
    # the same for every city page, not the whole rendered page, so
    # {% csrf_token %} in this template always gets a fresh token instead of a
    # stale one baked into a cached page.
    shared_data = cache.get('city_tour_shared_data')
    if shared_data is None:
        shared_data = {
            'items': spacial_destinations.objects.select_related('country', 'city').filter(show_homepage=True),
            'tours_country_list': get_tours_country_list(),
            'airlines': AirLineData.objects.all(),
            'footer_2': get_colm_two_pages(),
            'footer_3': get_colm_tree_pages(),
        }
        cache.set('city_tour_shared_data', shared_data, 60 * 10)

    theme_setting = index_page.objects.get(id=1)
    city_media = CityCountryMedia.objects.filter(city_id = id, is_active = True).order_by('sort_order', '-created_at')
    faqs = cityFAQ.objects.filter(Cityfaq=menu)
    forms = SearchForm()
    meta_robots = menu.tour_meta_robots

    tourlist = get_city_tours(menu.id)
    page_number = request.GET.get('page', 1)
    paginator = Paginator(tourlist, 11)
    tourlist = paginator.get_page(page_number)
    packages = []
    tour_cities = []
    dates = []
    card_packages = tour_card_packages_bulk(list(tourlist))
    for tour in tourlist:
        packages.append(card_packages.get(tour.id, []))

        tour_cities.append(
         list(TourCity.objects.filter(TourName=tour).select_related('Airline', 'FromAirport', 'ToAirport'))
        )

        dates.append(
         date_plan.objects.filter(tour=tour).exclude(start_date=tour.StartDate).count()
        )
    alldata = list(zip(tourlist, packages, tour_cities, dates))

    context = {
        'Search': forms,
        'city': menu,
        'media_list': city_media,
        'all_faqs': faqs,
        'set': theme_setting,
        'footer_2': shared_data['footer_2'],
        'footer_3': shared_data['footer_3'],
        'tour_countries': shared_data['tours_country_list'],
        'spacialDest': shared_data['items'],
        'airlines': shared_data['airlines'],
        'meta_robots': meta_robots,
        'pubTours': alldata,
        'tours_list': tourlist,
        # Legacy mobile template compatibility (keep the old mobile UI intact)
        'AllTour': tourlist,
        'AllData': list(zip(tourlist, tour_cities, packages)),
        'Menu': menu,
    }
    # تقویم جلالی (django_jalali.js + jquery-ui.min.css) فقط برای فرم‌هایی
    # لازم است که ورودی تاریخ دارند. این صفحه ندارد، ولی ۸۲ کیلوبایت را
    # روی هر بازدید دانلود می‌کرد.
    context['skip_jalali_datepicker'] = True
    return render(request, 'ui/all-tour.html', context)
def AllTourList(request):
    view = viewCounter.objects.get(id=1)
    view.toursView += 1
    view.save()

    # Same reasoning as IndexPage: cache the expensive, non-page-specific reads
    # instead of the whole rendered page, so {% csrf_token %} in this template
    # always gets a fresh token instead of a stale one baked into a cached page.
    all_tour_data = cache.get('all_tour_list_data')
    if all_tour_data is None:
        all_tour_data = {
            'items_tour': spacial_destinations.objects.select_related('country', 'city').filter(show_tourpage=True),
            'items': spacial_destinations.objects.select_related('country', 'city').filter(show_homepage=True),
            'tours_country_list': get_tours_country_list(),
            'reseller_menu': get_top_pages(),
            'footer_2': get_colm_two_pages(),
            'footer_3': get_colm_tree_pages(),
            'countries': get_tours_country(),
            'airlines': get_pub_tour_airlines(),
            'all_faqs': faq_home.objects.all(),
        }
        cache.set('all_tour_list_data', all_tour_data, 60 * 10)

    dest_cities = get_tours_cities
    forms = SearchForm()
    theme_setting = index_page.objects.get(id=1)
    meta_robots = 'INDEX,FOLLOW'
    # Moved to `python manage.py rollover_tour_dates` (scheduled task) — same
    # ~1250-query cost as IndexPage, running on every /all-tour cache-miss request.


    tourlist = get_all_pub_tours()
    page_number = request.GET.get('page', 1)
    paginator = Paginator(tourlist, 11)
    tourlist = paginator.get_page(page_number)
    packages = []
    tour_cities = []
    dates = []
    page_tours = list(tourlist)
    tour_ids = [tour.id for tour in page_tours]
    card_packages = tour_card_packages_bulk(page_tours)
    cities_by_tour = {}
    for tour_city in TourCity.objects.filter(TourName_id__in=tour_ids).select_related('Airline', 'FromAirport', 'ToAirport'):
        cities_by_tour.setdefault(tour_city.TourName_id, []).append(tour_city)
    starts_by_tour = {}
    for tour_id, start_date in date_plan.objects.filter(tour_id__in=tour_ids).values_list('tour_id', 'start_date'):
        starts_by_tour.setdefault(tour_id, []).append(start_date)
    for tour in page_tours:
        packages.append(card_packages.get(tour.id, []))
        tour_cities.append(cities_by_tour.get(tour.id, []))
        dates.append(len([
            start_date for start_date in starts_by_tour.get(tour.id, [])
            if start_date is not None and start_date != tour.StartDate
        ]))
    alldata = list(zip(page_tours, packages, tour_cities, dates))

    context = {
        'reseller_menu': all_tour_data['reseller_menu'],
        'Search': forms,
        'all_faqs': all_tour_data['all_faqs'],
        'set': theme_setting,
        'countries': all_tour_data['countries'],
        'footer_2': all_tour_data['footer_2'],
        'footer_3': all_tour_data['footer_3'],
        'tour_countries': all_tour_data['tours_country_list'],
        'dest_cities': dest_cities,
        'airlines': all_tour_data['airlines'],
        'spacialDest': all_tour_data['items'],
        'spacialDest_tour': all_tour_data['items_tour'],
        'meta_robots': meta_robots,
        'pubTours': alldata,
        'tours_list': tourlist,
        # Legacy mobile template compatibility (keep the old mobile UI intact)
        'AllTour': tourlist,
        'AllData': list(zip(tourlist, tour_cities, packages)),
    }
    # تقویم جلالی (django_jalali.js + jquery-ui.min.css) فقط برای فرم‌هایی
    # لازم است که ورودی تاریخ دارند. این صفحه ندارد، ولی ۸۲ کیلوبایت را
    # روی هر بازدید دانلود می‌کرد.
    context['skip_jalali_datepicker'] = True
    return render(request, 'ui/all-tour.html', context)

def MenuTourList(request, slug):
    try:
        menu = TourMenu.objects.get(slug=slug)
    except TourMenu.DoesNotExist:
        raise Http404
    top_menu = TourMenu.objects.filter(show_meu=True)
    items = spacial_destinations.objects.select_related('country', 'city').filter(show_homepage=True)
    items_2 = spacial_destinations.objects.select_related('country', 'city').filter(show_homepage=True)
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

# def tour_category_detail(request, slug):
#     category = get_object_or_404(
#         CustomTourCategory,
#         slug=slug
#     )
#     faqs = TourCategoryFAQ.objects.filter(category=category)

#     context = {
#         'category': category,
#         'category_title': category.name,
#         'category_desc': category.description,
#         'countries': get_tours_country(),
#         'tour_countries': get_tours_country_list(),
#         'dest_cities': get_tours_cities(),
#         'airlines': get_pub_tour_airlines(),
#         'spacialDest': spacial_destinations.objects.select_related('country', 'city').filter(show_homepage=True),
#         'spacialDest_tour': spacial_destinations.objects.select_related('country', 'city').filter(show_tourpage=True),
#         'all_faqs': faqs,
#         'meta_robots': category.meta_robots,
#     }
#     return render(
#         request,
#         'ui/all-tour.html',
#         context
#     )

def tour_category_detail(request, slug):
    category = get_object_or_404(
        CustomTourCategory,
        slug=slug
    )

    category_breadcrumbs = []
    current_category = category
    seen_categories = set()
    while current_category and current_category.id not in seen_categories:
        category_breadcrumbs.insert(0, current_category)
        seen_categories.add(current_category.id)
        current_category = current_category.parent

    faqs = TourCategoryFAQ.objects.filter(category=category)
    # tourlist = Tour.objects.filter(
    #     custom_categories=category,
    #     PubTour=True
    # ).order_by('-id')

    base_tour_qs = Tour.objects.filter(
        custom_categories=category,
        PubTour=True
    ).select_related(
        'Tcountry',
        'Tcity'
    ).distinct().order_by('-id')

    category_country = None
    category_city = None
    active_child_categories = CustomTourCategory.objects.none()
    if not category.parent_id:
        child_category_ids_with_tours = Package.objects.filter(
            TourName__custom_categories__parent=category,
            TourName__custom_categories__is_active=True,
            TourName__PubTour=True
        ).values_list(
            'TourName__custom_categories__id',
            flat=True
        ).distinct()
        active_child_categories = CustomTourCategory.objects.filter(
            parent=category,
            is_active=True,
            id__in=child_category_ids_with_tours
        ).distinct()
    first_tour_for_breadcrumb = base_tour_qs.exclude(
        Tcountry__isnull=True
    ).first()
    if first_tour_for_breadcrumb:
        category_country = first_tour_for_breadcrumb.Tcountry
    if category.parent_id:
        first_city_tour_for_breadcrumb = base_tour_qs.exclude(
            Tcity__isnull=True
        ).first()
        if first_city_tour_for_breadcrumb:
            category_city = first_city_tour_for_breadcrumb.Tcity
    # country_ids = list(
    #     base_tour_qs.exclude(Tcountry__isnull=True)
    #     .values_list('Tcountry_id', flat=True)
    #     .distinct()
    # )

    # if len(country_ids) == 1:
    #     category_country = Country.objects.filter(id=country_ids[0]).first()
    # first_tour_for_breadcrumb = base_tour_qs.exclude(
    #     Tcountry__isnull=True
    # ).first()

    # if first_tour_for_breadcrumb:
    #     category_country = first_tour_for_breadcrumb.Tcountry

    # if category.parent_id:
    #     city_ids = list(
    #         base_tour_qs.exclude(Tcity__isnull=True)
    #         .values_list('Tcity_id', flat=True)
    #         .distinct()
    #     )

    #     if len(city_ids) == 1:
    #         category_city = City.objects.filter(id=city_ids[0]).first()
    # if category.parent_id:
    #     first_city_tour_for_breadcrumb = base_tour_qs.exclude(
    #          Tcity__isnull=True
    #     ).first()
    # if first_city_tour_for_breadcrumb:
    #     category_city = first_city_tour_for_breadcrumb.Tcity

    tourlist = base_tour_qs

    page_number = request.GET.get('page', 1)
    paginator = Paginator(tourlist, 11)
    tourlist = paginator.get_page(page_number)
    packages = []
    tour_cities = []
    dates = []
    card_packages = tour_card_packages_bulk(list(tourlist))
    for tour in tourlist:
        packages.append(card_packages.get(tour.id, []))

        tour_cities.append(
            TourCity.objects.filter(
                TourName=tour
            )
        )

        dates.append(
            date_plan.objects.filter(
                tour=tour
            ).count()
        )
    alldata = list(zip(tourlist, packages, tour_cities, dates))
    context = {
        'category': category,
        'category_title': category.name,
        'category_desc': category.description,
        'category_breadcrumbs': category_breadcrumbs,
        'category_country': category_country,
        'category_city': category_city,
        'active_child_categories': active_child_categories,
        'countries': get_tours_country(),
        'tour_countries': get_tours_country_list(),
        'dest_cities': get_tours_cities(),
        'airlines': get_pub_tour_airlines(),
        'spacialDest': spacial_destinations.objects.select_related('country', 'city').filter(show_homepage=True),
        'spacialDest_tour': spacial_destinations.objects.select_related('country', 'city').filter(show_tourpage=True),
        'all_faqs': faqs,
        'meta_robots': category.meta_robots,
        'pubTours': alldata,
        'tours_list': tourlist,
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
        cities.append(list(TourCity.objects.filter(TourName_id=i).select_related('Airline', 'FromAirport', 'ToAirport')))
    paginator = Paginator(tours, 10)
    PageNumber = request.GET.get('page')
    tours = paginator.get_page(PageNumber)
    packages = []
    card_packages = tour_card_packages_bulk(list(tours))
    for i in tours:
        packages.append(card_packages.get(i.id, []))
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
    # تقویم جلالی (django_jalali.js + jquery-ui.min.css) فقط برای فرم‌هایی
    # لازم است که ورودی تاریخ دارند. این صفحه ندارد، ولی ۸۲ کیلوبایت را
    # روی هر بازدید دانلود می‌کرد.
    context['skip_jalali_datepicker'] = True
    if request.user_agent.is_mobile:
        return render(request, 'ui/mobile/all-tour.html', context)
    else:
        return render(request, 'ui/all-tour.html', context)
# عمداً @cache_page ندارد. این قالب فرم «درخواست رزرو» را با {% csrf_token %}
# رندر می‌کند؛ اگر کل صفحه کش شود، توکن CSRFِ یک بازدیدکننده داخل HTML پخته
# می‌شود و به بقیه هم همان تحویل می‌رود، در حالی که کوکی csrftoken آن‌ها فرق
# دارد (یا اصلاً ست نمی‌شود، چون روی cache hit میان‌افزار CSRF اجرا نمی‌شود).
# نتیجه: ارسال فرم رزرو با 403 رد می‌شود. مثل AllTourList/CategoryTourList
# فقط داده‌های مشترک کش می‌شوند، نه خروجی رندرشده.
def TourDetail(request,id, Slug):
    items = spacial_destinations.objects.select_related('country', 'city').filter(show_homepage=True)
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
    date_plans = date_plan.objects.filter(tour=tour).exclude(start_date=tour.StartDate).order_by('start_date')
    selected_dp = None
    dp_id = request.GET.get('dp')
    if dp_id:
        try:
            selected_dp = date_plan.objects.get(id=dp_id, tour=tour)
        except date_plan.DoesNotExist:
            pass
    # اگه یه date_plan دقیقاً با تاریخ پیش‌فرض تور یکی باشه، از تب تاریخ‌ها حذف میشه
    # (چون تکراریه) ولی خودش هیچ‌وقت با dp دستی هم قابل انتخاب نیست؛ پس تنظیمات
    # (قیمت/پکیج مخصوص/تکمیل ظرفیت و ...) اون باید خودکار روی همین نمایش پیش‌فرض اعمال بشه
    base_date_plan = date_plan.objects.filter(tour=tour, start_date=tour.StartDate).first()
    if selected_dp is None and base_date_plan:
        selected_dp = base_date_plan
    tipe_plan = TripPlan.objects.filter(tour=tour).order_by('id')
    cities = list(TourCity.objects.filter(TourName_id=tour.id).select_related('Airline', 'FromAirport', 'ToAirport'))
    # packages = list(Package.objects.filter(TourName=tour.id).order_by('DoubleBedPrice', 'DoubleBedPrice_doller'))
    exclusive_filter = Q(exclusive_date_plan__isnull=True)
    if selected_dp:
        exclusive_filter |= Q(exclusive_date_plan_id=selected_dp.id)
    packages = list(
        Package.objects.filter(TourName=tour.id)
        .filter(exclusive_filter)
        .select_related('HotelName', 'Mhotel', 'M1hotel', 'M2hotel', 'M3hotel')
        .prefetch_related(
            'HotelName__hotel_images_set',
            'Mhotel__hotel_images_set',
            'M1hotel__hotel_images_set',
            'M2hotel__hotel_images_set',
            'M3hotel__hotel_images_set',
        )
        .order_by('DoubleBedPrice', 'DoubleBedPrice_doller')
    )
    _SOLDOUT_SLOTS = [
        ('hotel', 'hotel_sold_out', 'HotelName'),
        ('mhotel', 'mhotel_sold_out', 'Mhotel'),
        ('m1hotel', 'm1hotel_sold_out', 'M1hotel'),
        ('m2hotel', 'm2hotel_sold_out', 'M2hotel'),
        ('m3hotel', 'm3hotel_sold_out', 'M3hotel'),
    ]
    def _compute_fully_sold_out(pkg):
        assigned = [slot for slot, _, hotel_attr in _SOLDOUT_SLOTS if getattr(pkg, hotel_attr)]
        return bool(assigned) and all(pkg.sold_out_map[slot] for slot in assigned)
    _HOTEL_OVERRIDE_ATTRS = [
        ('HotelName', 'hotel_override'),
        ('Mhotel', 'mhotel_override'),
        ('M1hotel', 'm1hotel_override'),
        ('M2hotel', 'm2hotel_override'),
        ('M3hotel', 'm3hotel_override'),
    ]
    _VIEW_SERVICE_OVERRIDE_ATTRS = [
        ('view_hotel', 'service_hotel'),
        ('view_mhotel', 'service_mhotel'),
        ('view_m1hotel', 'service_m1hotel'),
        ('view_m2hotel', 'service_m2hotel'),
        ('view_m3hotel', 'service_m3hotel'),
    ]
    _TRANSFER_SLOTS = [
        ('mhotel', 'transfer_mhotel', 'HotelName', 'Mhotel'),
        ('m1hotel', 'transfer_m1hotel', 'Mhotel', 'M1hotel'),
        ('m2hotel', 'transfer_m2hotel', 'M1hotel', 'M2hotel'),
        ('m3hotel', 'transfer_m3hotel', 'M2hotel', 'M3hotel'),
    ]
    _TRANSFER_LABELS = {
        'bus': 'اتوبوس',
        'train': 'قطار',
        'flight': 'پرواز داخلی',
        'boat': 'قایق',
    }
    def _leg_kind(city):
        if city.GTransfer:
            return 'bus'
        if city.QTransfer:
            return 'train'
        if city.STransfer:
            return 'boat'
        if city.flight_inbound:
            return 'flight'
        return ''

    transfer_by_pair = {}
    transfer_by_city = {}
    for position, city in enumerate(cities):
        kind = _leg_kind(city)
        if not kind or not city.CtName_id:
            continue
        transfer_by_city.setdefault(city.CtName_id, kind)
        next_city = cities[position + 1] if position + 1 < len(cities) else None
        if next_city is not None and next_city.CtName_id:
            transfer_by_pair.setdefault((city.CtName_id, next_city.CtName_id), kind)

    def _transfer_for(pkg, field, leaving_attr, arriving_attr):
        chosen = getattr(pkg, field, '') or ''
        if chosen:
            return chosen
        leaving = getattr(pkg, leaving_attr, None)
        arriving = getattr(pkg, arriving_attr, None)
        if leaving is None or arriving is None:
            return ''
        if leaving.Hcity_id == arriving.Hcity_id:
            return ''
        paired = transfer_by_pair.get((leaving.Hcity_id, arriving.Hcity_id))
        if paired:
            return paired
        return transfer_by_city.get(leaving.Hcity_id, '')

    for pkg in packages:
        pkg.sold_out_map = {slot: getattr(pkg, field) for slot, field, _ in _SOLDOUT_SLOTS}
        pkg.fully_sold_out = _compute_fully_sold_out(pkg)
        pkg.is_hidden_for_date = False
        pkg.transfer_map = {
            slot: _transfer_for(pkg, field, leaving_attr, arriving_attr)
            for slot, field, leaving_attr, arriving_attr in _TRANSFER_SLOTS
        }
        pkg.transfer_label_map = {
            slot: _TRANSFER_LABELS.get(kind, '') for slot, kind in pkg.transfer_map.items()
        }
    # «ارزون‌ترین قیمت» هر تاریخ باید واقعاً بین همه‌ی پکیج‌های قابل‌نمایش همون تاریخ
    # حساب بشه (نه فقط یک پکیجِ ثابتِ از پیش انتخاب‌شده) وگرنه با تغییر قیمت/افزودن
    # پکیج برای بقیه‌ی پکیج‌ها، تب‌های تاریخ به‌روز نمی‌شدن
    _all_packages_for_pricing = list(
        Package.objects.filter(TourName=tour.id).select_related('Pcry', 'fr_Pcry')
    )
    base_best = compute_tour_min_price(_all_packages_for_pricing, base_date_plan)
    if base_best:
        base_price = base_best['price']
        base_price_dollar = base_best['price_dollar']
        base_currency = base_best['currency']
        base_currency_foreign = base_best['currency_foreign']
    else:
        base_price = 0
        base_price_dollar = 0
        base_currency = 'تومان'
        base_currency_foreign = 'دلار'
    _fa_days = ['دوشنبه', 'سه‌شنبه', 'چهارشنبه', 'پنجشنبه', 'جمعه', 'شنبه', 'یکشنبه']
    tour_start_weekday = _fa_days[tour.StartDate.weekday()] if tour.StartDate else ''
    date_plans_with_price = []
    for dp_item in date_plans:
        item_best = compute_tour_min_price(_all_packages_for_pricing, dp_item)
        fp = item_best['price'] if item_best else base_price
        fp_dollar = item_best['price_dollar'] if item_best else base_price_dollar
        color = 'up' if fp > base_price else 'down' if fp < base_price else 'neutral'
        weekday = _fa_days[dp_item.start_date.weekday()] if dp_item.start_date else ''
        date_plans_with_price.append({'dp': dp_item, 'final_price': fp, 'final_price_dollar': fp_dollar, 'weekday': weekday, 'color': color})
    base_dp_color = 'neutral'
    if selected_dp:
        adj = int(selected_dp.price or 0)
        adj_foreign = int(selected_dp.price_dollar or 0)
        adj_infant = int(selected_dp.infant_price or 0)
        adj_infant_foreign = int(selected_dp.infant_price_dollar or 0)
        dollar_type = selected_dp.price_dollar_type
        if dollar_type not in ('افزایش', 'کاهش'):
            dollar_type = selected_dp.price_type
        sign = 1 if selected_dp.price_type == 'افزایش' else -1 if selected_dp.price_type == 'کاهش' else 0
        sign_f = 1 if dollar_type == 'افزایش' else -1 if dollar_type == 'کاهش' else 0
        package_overrides = {
            o.package_id: o
            for o in DatePlanPackagePrice.objects.filter(
                date_plan=selected_dp, package_id__in=[p.id for p in packages]
            ).select_related('hotel_override', 'mhotel_override', 'm1hotel_override', 'm2hotel_override', 'm3hotel_override')
        }
        for pkg in packages:
            override = package_overrides.get(pkg.id)
            if override:
                for hotel_attr, override_field in _HOTEL_OVERRIDE_ATTRS:
                    override_hotel = getattr(override, override_field)
                    if override_hotel:
                        setattr(pkg, hotel_attr, override_hotel)
                for view_field, service_field in _VIEW_SERVICE_OVERRIDE_ATTRS:
                    if getattr(override, view_field):
                        setattr(pkg, view_field, getattr(override, view_field))
                    if getattr(override, service_field):
                        setattr(pkg, service_field, getattr(override, service_field))
                if override.main_pkg_id:
                    pkg.MainPkg_id = override.main_pkg_id
                if override.currency_id:
                    pkg.Pcry_id = override.currency_id
                if override.foreign_currency_id:
                    pkg.fr_Pcry_id = override.foreign_currency_id
                if override.view:
                    pkg.view = override.view
                if override.doller_price:
                    pkg.DollerPrice = override.doller_price
                pkg.sold_out_map = {slot: getattr(override, field) for slot, field, _ in _SOLDOUT_SLOTS}
                pkg.fully_sold_out = _compute_fully_sold_out(pkg)
                pkg.is_hidden_for_date = override.is_hidden
                pkg.DoubleBedPrice = override.DoubleBedPrice
                pkg.SingleBedPrice = override.SingleBedPrice
                pkg.BabyWithBedPrice = override.BabyWithBedPrice
                pkg.BabyWithoutBedPrice = override.BabyWithoutBedPrice
                pkg.InfontPrice = override.InfontPrice
                pkg.DoubleBedPrice_doller = override.DoubleBedPrice_doller
                pkg.SingleBedPrice_doller = override.SingleBedPrice_doller
                pkg.BabyWithBedPrice_doller = override.BabyWithBedPrice_doller
                pkg.BabyWithoutBedPrice_doller = override.BabyWithoutBedPrice_doller
                pkg.InfontPrice_doller = override.InfontPrice_doller
            elif pkg.exclusive_date_plan_id:
                # پکیج مخصوص همین تاریخه؛ قیمتش از قبل مستقیماً برای همین تاریخ ثبت شده
                # (نه یک override جدا)، پس نباید اختلاف‌قیمت عمومی تاریخ رویش دوباره اعمال بشه
                pass
            else:
                pkg.DoubleBedPrice = (pkg.DoubleBedPrice or 0) + sign * adj
                pkg.SingleBedPrice = (pkg.SingleBedPrice or 0) + sign * adj
                pkg.BabyWithBedPrice = (pkg.BabyWithBedPrice or 0) + sign * adj
                pkg.BabyWithoutBedPrice = (pkg.BabyWithoutBedPrice or 0) + sign * adj
                pkg.InfontPrice = (pkg.InfontPrice or 0) + sign * adj_infant
                pkg.DoubleBedPrice_doller = (pkg.DoubleBedPrice_doller or 0) + sign_f * adj_foreign
                pkg.SingleBedPrice_doller = (pkg.SingleBedPrice_doller or 0) + sign_f * adj_foreign
                pkg.BabyWithBedPrice_doller = (pkg.BabyWithBedPrice_doller or 0) + sign_f * adj_foreign
                pkg.BabyWithoutBedPrice_doller = (pkg.BabyWithoutBedPrice_doller or 0) + sign_f * adj_foreign
                pkg.InfontPrice_doller = (pkg.InfontPrice_doller or 0) + sign_f * adj_infant_foreign
        packages = [pkg for pkg in packages if not pkg.is_hidden_for_date]
    related_tour = Tour.objects.filter(Tcity=tour.Tcity, PubTour=True).exclude(pk=tour.id).order_by('-id')[:4]
    related_packages = []
    _related_bulk = tour_card_packages_bulk(list(related_tour))
    for i in related_tour:
        related_packages.append(_related_bulk.get(i.id, []))
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
        'selected_dp': selected_dp,
        'base_date_plan_id': base_date_plan.id if base_date_plan else None,
        'date_plans_with_price': date_plans_with_price,
        'base_price': base_price,
        'base_dp_color': base_dp_color,
        'Order': form2,
        'Search': forms,
        'set':theme_setting,
        'gallery': gallery,
        'tour_countries': tours_country_list,
        'tipe_plan': tipe_plan,
        'spacialDest': items,
        'meta_robots': tour.meta_robots,
        'tour_start_weekday': tour_start_weekday,
        'base_price_dollar': base_price_dollar,
        'base_currency': base_currency,
        'base_currency_foreign': base_currency_foreign,
    }
    # تقویم جلالی (django_jalali.js + jquery-ui.min.css) فقط برای فرم‌هایی
    # لازم است که ورودی تاریخ دارند. این صفحه ندارد، ولی ۸۲ کیلوبایت را
    # روی هر بازدید دانلود می‌کرد.
    context['skip_jalali_datepicker'] = True
    return render(request, 'ui/detail-tour.html', context)
def AllHotelList(request):
    items = spacial_destinations.objects.select_related('country', 'city').filter(show_homepage=True)
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
    items = spacial_destinations.objects.select_related('country', 'city').filter(show_homepage=True)
    tours_country_list = get_tours_country_list()
    theme_setting = index_page.objects.get(id=1)
    try:
        hotelmenu = Country.objects.get(slug=slug)
    except Country.DoesNotExist:
        raise Http404
    hotels = get_all_country_hotels(hotelmenu.id)
    all_faqs = hotel_faq_Country.objects.filter(Countryfaq=hotelmenu)
    paginator = Paginator(hotels.select_related('Hcity'), 12)
    PageNumber = request.GET.get('page')
    hotels = paginator.get_page(PageNumber)
    city_set = set(h.Hcity for h in get_all_country_hotels(hotelmenu.id).select_related('Hcity').only('id', 'Hcity'))
    city_totals = dict(Hotel_Data.objects.filter(Hcity__in=[c.pk for c in city_set]).order_by().values_list('Hcity').annotate(total=M.Count('id')))
    cities_hotels_number = [(c, city_totals.get(c.pk, 0)) for c in city_set]
    formsub = SubscribeForm()
    if request.method == 'POST':
        formsub = SubscribeForm(request.POST)
        if formsub.is_valid():
            formsub.save()
            return redirect('/')

    meta_robots = hotelmenu.hotel_meta_robots

    context = {
        'Hotels': hotels,
        'country': hotelmenu,
        'all_faqs': all_faqs,
        'set': theme_setting,
        'cities': cities_hotels_number,
        'tour_countries': tours_country_list,
        'spacialDest': items,
        "type": "country",
        'meta_robots': meta_robots,
        'skip_jalali_datepicker': True,
    }
    return render(request, 'ui/all-hotel-list.html', context)

def AllHotelCity(request, id, slug):
    items = spacial_destinations.objects.select_related('country', 'city').filter(show_homepage=True)
    tours_country_list = get_tours_country_list()
    theme_setting = index_page.objects.get(id=1)
    hotelmenu = City.objects.filter(id=id, slug=slug).first() or City.objects.filter(slug=slug).order_by('id').first()
    if hotelmenu is None:
        raise Http404
    all_faqs = hotel_faq_city.objects.filter(Cityfaq=hotelmenu)    
    meta_robots = hotelmenu.hotel_meta_robots
    hotels = Paginator(get_all_city_hotels(hotelmenu.id).select_related('Hcity'), 12).get_page(1)

    context = {
        'Hotels': hotels,
        'city': hotelmenu,
        'all_faqs': all_faqs,
        'set': theme_setting,
        'tour_countries': tours_country_list,
        'spacialDest': items,
        'type': 'city',
        'meta_robots': meta_robots,
        'skip_jalali_datepicker': True,
    }
    return render(request, 'ui/all-hotel-list.html', context)

def hotel_search(request):
    items = spacial_destinations.objects.select_related('country', 'city').filter(show_homepage=True)
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
    items = spacial_destinations.objects.select_related('country', 'city').filter(show_homepage=True)
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
    for slot in ('HotelName', 'Mhotel', 'M1hotel', 'M2hotel', 'M3hotel'):
        packages.extend(Package.objects.filter(
            **{slot: hotel}, TourName__PubTour=True, exclusive_date_plan__isnull=True
        ).select_related('TourName', 'TourName__Tcountry', 'Pcry'))
    packages = apply_own_base_price_bulk(list(set(packages)))
    has_desc = bool(unescape(strip_tags(hotel.HotelDesc or '')).replace(chr(0x200c), '').strip())
    tour_city = tour_country = None
    if (Tour.objects.filter(Tcity_id=hotel.Hcity_id, PubTour=True).exists()
            or related_tour_city.objects.filter(city_id=hotel.Hcity_id, tour__PubTour=True).exists()):
        tour_city = hotel.Hcity
    elif packages:
        tour_city = max(packages, key=lambda p: p.TourName_id).TourName.Tcity
    if tour_city is None and (Tour.objects.filter(Tcountry_id=hotel.Hcountry_id, PubTour=True).exists()
            or related_tour_city.objects.filter(country_id=hotel.Hcountry_id, tour__PubTour=True).exists()):
        tour_country = hotel.Hcountry
    Hotel_Data.objects.filter(pk=hotel.pk).update(viewCount=M.F('viewCount') + 1)
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
        'has_desc': has_desc,
        'tour_city': tour_city,
        'tour_country': tour_country,
        'tour_countries': tours_country_list,
        'spacialDest': items,
        'comments_form': comments_form,
        'all_comments': all_comments,
        'Lcordinate':cordinate[0],
        'Acordinate':cordinate[1],
        'meta_robots': hotel.meta_robots,
        'skip_jalali_datepicker': True,
    }
    return render(request, 'ui/hotel-detail.html', context)

def TourSearch(request):
    items = spacial_destinations.objects.select_related('country', 'city').filter(show_homepage=True)
    tours_country_list = get_tours_country_list()
    select_countries =  Country.objects.all()
    country = request.POST.get('country_id')
    pubTours = get_all_pub_tours()
    cities = City.objects.all()
    if country:
        country = int(country)
        pubTours = pubTours.filter(Tcountry=country)
        cities = City.objects.filter(CountryName=country)
    city = request.POST.get('city_id')
    if city :
        city = int(city)
        pubTours = pubTours.filter(Tcity=city)
    day = request.POST.get('day_count')
    if day:
        day = int(day)
        pubTours = pubTours.filter(DayCount=day)
    # قبلاً لیست پکیج‌ها اصلاً به تور متناظرش وصل نمی‌شد (همه‌ی پکیج‌های سایت zip
    # می‌شدن) و قیمت اشتباه رو کارت نتایج جستجو نشون داده می‌شد
    _bulk = tour_card_packages_bulk(list(pubTours))
    packages = [_bulk.get(t.id, []) for t in pubTours]
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
@cache_page(60 * 30)
def BlogPage(request):
    items = spacial_destinations.objects.select_related('country', 'city').filter(show_homepage=True)
    visa_post = blogPosts.objects.get(id=16)
    tours_country_list = get_tours_country_list()
    theme_setting = index_page.objects.get(id=1)
    view = viewCounter.objects.get(id=1)
    view.blogView += 1
    view.save()
    posts = blogPosts.objects.filter(Publish=True).only('Title', 'Category', 'Image').order_by('-PubDate')[:6]
    fav_posts = blogPosts.objects.filter(Publish=True).only('Title', 'Category', 'Image').order_by('-viewCount')[:6]

    search_query = request.GET.get('q', '').strip()
    if search_query:
        all_posts = blogPosts.objects.filter(
            Publish=True
        ).filter(
            Q(Title__icontains=search_query) |
            Q(ShortDesc__icontains=search_query) |
            Q(Description__icontains=search_query)
        ).annotate(
            title_match=Case(
                When(Title__icontains=search_query, then=Value(0)),
                default=Value(1),
                output_field=IntegerField()
            )
        ).order_by('title_match', '-PubDate')
    else:
        all_posts = blogPosts.objects.filter(Publish=True).only('Title', 'Category', 'Image').order_by('-PubDate') 
    categories = PostCategory.objects.all()
    ch_categories = PostCategory.objects.exclude(parentCat=None)
    ch_cat_number = []
    for i in categories:
        ch_cat_number.append(PostCategory.objects.filter(parentCat=i).count())
    parent_categories = zip(categories, ch_cat_number)
    paginator = Paginator(all_posts, 10)
    pagenumber = request.GET.get('page')
    data = paginator.get_page(pagenumber)
    
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
        'meta_robots': meta_robots,
        'search_query': search_query,
    }
    return render(request, 'ui/blog.html', context)

def CategoryPost(request, id, slug):
    items = spacial_destinations.objects.select_related('country', 'city').filter(show_homepage=True)
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
@cache_page(60 * 30)
def PostDetail(request, id, slug):
    items = spacial_destinations.objects.select_related('country', 'city').filter(show_homepage=True)
    tours_country_list = get_tours_country_list()
    tset = index_page.objects.get(id=1)
    try:
        post = blogPosts.objects.get(id=id, slug=slug)
    except blogPosts.DoesNotExist:
        raise Http404
    blogPosts.objects.filter(id=post.id).update(viewCount=M.F("viewCount") + 1)
    post_related = related_posts.objects.filter(post=post).select_related(
        'related_post', 'related_post__Category').order_by('-id')
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
    context = {
        'Post': post,
        'Posts': post_related,
        'all_comments': all_comments,
        'all_comments_reply': all_comments_reply,
        'set': tset,
        'tour_countries': tours_country_list,
        'spacialDest': items,
        'meta_robots': post.meta_robots,
        'skip_jalali_datepicker': True,
    }
    return render(request, 'ui/post-detail.html', context)

def AboutUsUi(request):
    items = spacial_destinations.objects.select_related('country', 'city').filter(show_homepage=True)
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
    items = spacial_destinations.objects.select_related('country', 'city').filter(show_homepage=True)
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
    order = get_object_or_404(
        TourOrder.objects.select_related(
            'OrderTour', 'Orderpackage', 'Orderpackage__HotelName',
            'Orderpackage__MainPkg'),
        id=id, OrderCode=OrderCode)
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
    order = get_object_or_404(TourOrder, id=id, OrderCode=OrderCode)
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
    items = spacial_destinations.objects.select_related('country', 'city').filter(show_homepage=True)
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
    context['skip_jalali_datepicker'] = True
    return render(request, 'ui/single-memo.html', context)


def CategoryMemo(request, slug):
    items = spacial_destinations.objects.select_related('country', 'city').filter(show_homepage=True)
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
    context['skip_jalali_datepicker'] = True
    return render(request, 'tour/category-memo.html', context)


def handler404(request, *args, **argv):
    # status=404 لازم است: بدون آن صفحهٔ «پیدا نشد» با کد ۲۰۰ برمی‌گردد و
    # گوگل آدرس‌های نامعتبر را به‌عنوان صفحهٔ سالم ایندکس می‌کند (soft 404).
    return render(request, 'ui/404.html', status=404)


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
    items = spacial_destinations.objects.select_related('country', 'city').filter(show_homepage=True)
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