from django.shortcuts import render, redirect
from tour.forms import CreateCountryForm, faqCreateForm, CreateCityForm, cityfaqCreateForm, relatedCityForm, \
    faqhotelcountryCreateForm, cityfaqhotelCreateForm, CityCountryMediaForm, CreateTourCategoryFaqForm
from tour.models import City, Country, FAQ, cityFAQ, Tour, related_tour_city, hotel_faq_Country,\
    hotel_faq_city, CityCountryMedia, CustomTourCategory, TourCategoryFAQ
from django.core.paginator import Paginator
from tour.pms_manager import *
from django.contrib import messages

@superuser_required(login_url='login')
def create_country(request):
    form = CreateCountryForm()
    if request.method == 'POST':
        forms = CreateCountryForm(request.POST, request.FILES)
        if forms.is_valid():
            forms.save()
            return redirect('country_list')

    context = {
        'Form': form,
    }
    return render(request, 'tour/create-country.html', context)


@superuser_required(login_url='login')
def update_country(request, id):
    country = Country.objects.get(id=id)
    form = CreateCountryForm(instance=country)
    if request.method == 'POST':
        forms = CreateCountryForm(request.POST, request.FILES, instance=country)
        if forms.is_valid():
            forms.save()
            return redirect('country_list')

    context = {
        'Form': form,
        'country': country
    }
    return render(request, 'tour/create-country.html', context)


@superuser_required(login_url='login')
def delete_country(request, id):
    country = Country.objects.get(id=id)
    country.delete()
    return redirect('country_list')


@superuser_required(login_url='login')
def create_country_faq(request, id):
    tourmenu = Country.objects.get(id=id)
    form = faqCreateForm()
    if request.method == 'POST':
        forms = faqCreateForm(request.POST)
        if forms.is_valid():
            faq = forms.save(commit=False)
            faq.Countryfaq = tourmenu
            faq.save()
            return redirect('create-faq', tourmenu.id)
    context = {
        'FormSet': form,
        'Country': tourmenu,
    }
    return render(request, 'tour/create-faq.html', context)

@superuser_required(login_url='login')
def create_hotel_country_faq(request, id):
    country = Country.objects.get(id=id)
    form = faqCreateForm()
    if request.method == 'POST':
        forms = faqhotelcountryCreateForm(request.POST)
        if forms.is_valid():
            faq = forms.save(commit=False)
            faq.Countryfaq = country
            faq.save()
            return redirect('create_hotel_country_faq', country.id)
    context = {
        'FormSet': form,
        'Country': country,
    }
    return render(request, 'tour/create-hotel-faq.html', context)

@superuser_required(login_url='login')
def update_country_hotel_faq(request, id):
    faq = hotel_faq_Country.objects.get(id=id)
    country = Country.objects.get(id=faq.Countryfaq.id)
    form = faqhotelcountryCreateForm(instance=faq)
    if request.method == 'POST':
        forms = faqhotelcountryCreateForm(request.POST, instance=faq)
        if forms.is_valid():
            forms.save()
            return redirect('create_hotel_country_faq', faq.Countryfaq.id)
    allfaq = hotel_faq_Country.objects.filter(Countryfaq=country.id)
    paginator = Paginator(allfaq, 15)
    page_number = request.GET.get('page')
    faqlist = paginator.get_page(page_number)
    context = {
        'FormSet': form,
        'List': faqlist,
        'Country': country,
    }
    return render(request, 'tour/create-hotel-faq.html', context)

@superuser_required(login_url='login')
def update_country_faq(request, id):
    faq = FAQ.objects.get(id=id)
    tourmenu = Country.objects.get(id=faq.Countryfaq.id)
    form = faqCreateForm(instance=faq)
    if request.method == 'POST':
        forms = faqCreateForm(request.POST, instance=faq)
        if forms.is_valid():
            forms.save()
            return redirect('create-faq', faq.Countryfaq.id)
    allfaq = FAQ.objects.filter(Countryfaq=tourmenu.id)
    paginator = Paginator(allfaq, 15)
    page_number = request.GET.get('page')
    faqlist = paginator.get_page(page_number)
    context = {
        'FormSet': form,
        'List': faqlist,
        'Country': tourmenu,
    }
    return render(request, 'tour/create-faq.html', context)

@superuser_required(login_url='login')
def delete_country_hotel_faq(request, id):
    faq = hotel_faq_Country.objects.get(id=id)
    faq.delete()
    return redirect('country_list')

@superuser_required(login_url='login')
def delete_country_faq(request, id):
    faq = FAQ.objects.get(id=id)
    faq.delete()
    return redirect('country_list')

@superuser_required(login_url='login')
def country_hotel_faq_list(request, id):
    menu = Country.objects.get(id=id)
    allfaq = hotel_faq_Country.objects.filter(Countryfaq=menu.id)
    paginator = Paginator(allfaq, 15)
    page_number = request.GET.get('page')
    faqlist = paginator.get_page(page_number)
    context = {
        'Menu': menu,
        'List': faqlist
    }
    return render(request, 'tour/faq-list.html', context)

@superuser_required(login_url='login')
def country_faq_list(request, id):
    menu = Country.objects.get(id=id)
    allfaq = FAQ.objects.filter(Countryfaq=menu.id)
    paginator = Paginator(allfaq, 15)
    page_number = request.GET.get('page')
    faqlist = paginator.get_page(page_number)
    context = {
        'Menu': menu,
        'List': faqlist
    }
    return render(request, 'tour/faq-list.html', context)


@superuser_required(login_url='login')
def country_list(request):
    return render(request, 'destinations/country_list.html')


@superuser_required(login_url='login')
def create_city(request):
    form = CreateCityForm()
    if request.method == 'POST':
        forms = CreateCityForm(request.POST, request.FILES)
        if forms.is_valid():
            forms.save()
            return redirect('city_list')
    context = {
        'Form': form,
    }
    return render(request, 'tour/create-city.html', context)


@superuser_required(login_url='login')
def update_city(request, id):
    city = City.objects.get(id=id)
    form = CreateCityForm(instance=city)
    if request.method == 'POST':
        forms = CreateCityForm(request.POST, request.FILES, instance=city)
        if forms.is_valid():
            forms.save()
            return redirect('city_list')
    context = {
        'Form': form,
        'city': city
    }
    return render(request, 'tour/create-city.html', context)


@superuser_required(login_url='login')
def delete_city(request, id):
    city = City.objects.get(id=id)
    city.delete()
    return redirect('city_list')


@superuser_required(login_url='login')
def create_city_faq(request, id):
    tourmenu = City.objects.get(id=id)
    form = cityfaqCreateForm()
    if request.method == 'POST':
        forms = cityfaqCreateForm(request.POST)
        if forms.is_valid():
            faq = forms.save(commit=False)
            faq.Cityfaq = tourmenu
            faq.save()
            return redirect('create-city-faq', tourmenu.id)
    context = {
        'FormSet': form,
        'city': tourmenu,
    }
    return render(request, 'tour/create-city-faq.html', context)

@superuser_required(login_url='login')
def create_tour_category_faq(request, id):
    category = CustomTourCategory.objects.get(id=id)
    form = CreateTourCategoryFaqForm()
    if request.method == 'POST':
        forms = CreateTourCategoryFaqForm(request.POST)
        if forms.is_valid():
            faq = forms.save(commit=False)
            faq.category = category
            faq.save()
            return redirect('create-tour-category-faq', category.id)
    context = {
        'FormSet': form,
        'category': category,
    }
    return render(request, 'tour/create-tour-category-faq.html', context)

@superuser_required(login_url='login')
def update_tour_category_faq(request, id):
    faq = TourCategoryFAQ.objects.get(id=id)
    category = CustomTourCategory.objects.get(id=faq.category.id)
    form = CreateTourCategoryFaqForm(instance=faq)
    if request.method == 'POST':
        forms = CreateTourCategoryFaqForm(request.POST, instance=faq)
        if forms.is_valid():
            forms.save()
            return redirect('create-tour-category-faq', faq.category.id)
    context = {
        'FormSet': form,
        'category': category,
    }
    return render(request, 'tour/create-tour-category-faq.html', context)

@superuser_required(login_url='login')
def delete_tour_category_faq(request, id):
    faq = TourCategoryFAQ.objects.get(id=id)
    category = faq.category.id
    faq.delete()
    return redirect('create-tour-category-faq', category)

@superuser_required(login_url='login')
def create_city_hotel_faq(request, id):
    tourmenu = City.objects.get(id=id)
    form = cityfaqhotelCreateForm()
    if request.method == 'POST':
        forms = cityfaqhotelCreateForm(request.POST)
        if forms.is_valid():
            faq = forms.save(commit=False)
            faq.Cityfaq = tourmenu
            faq.save()
            return redirect('create_city_hotel_faq', tourmenu.id)
    context = {
        'FormSet': form,
        'city': tourmenu,
    }
    return render(request, 'tour/create-city-hotel-faq.html', context)


@superuser_required(login_url='login')
def update_city_faq(request, id):
    faq = cityFAQ.objects.get(id=id)
    tourmenu = City.objects.get(id=faq.Cityfaq.id)
    form = cityfaqCreateForm(instance=faq)
    if request.method == 'POST':
        forms = cityfaqCreateForm(request.POST, instance=faq)
        if forms.is_valid():
            forms.save()
            return redirect('create-city-faq', faq.Cityfaq.id)
    context = {
        'FormSet': form,
        'city': tourmenu,
    }
    return render(request, 'tour/create-city-faq.html', context)

@superuser_required(login_url='login')
def update_city_hotel_faq(request, id):
    faq = hotel_faq_city.objects.get(id=id)
    tourmenu = City.objects.get(id=faq.Cityfaq.id)
    form = cityfaqhotelCreateForm(instance=faq)
    if request.method == 'POST':
        forms = cityfaqhotelCreateForm(request.POST, instance=faq)
        if forms.is_valid():
            forms.save()
            return redirect('create_city_hotel_faq', faq.Cityfaq.id)
    context = {
        'FormSet': form,
        'city': tourmenu,
    }
    return render(request, 'tour/create-city-hotel-faq.html', context)

@superuser_required(login_url='login')
def delete_city_faq(request, id):
    faq = cityFAQ.objects.get(id=id)
    city = faq.Cityfaq.id
    faq.delete()
    return redirect('create-city-faq', city)

@superuser_required(login_url='login')
def delete_city_hotel_faq(request, id):
    faq = hotel_faq_city.objects.get(id=id)
    city = faq.Cityfaq.id
    faq.delete()
    return redirect('create_city_hotel_faq', city)

@superuser_required(login_url='login')
def create_media_city(request, id):
    city = City.objects.get(id=id)
    forms = CityCountryMediaForm()
    
    if request.method == 'POST':
        
        forms = CityCountryMediaForm(request.POST, request.FILES)
        
        if forms.is_valid():
            media = forms.save(commit=False)
            media.city = city
            media.save()
            
            messages.success(request, f'رسانه "{media.title}" با موفقیت اضافه شد.')
            return redirect('create-media-city', city.id)
        
    context = {
        'FormSet': forms,
        'city': city,
    }
    return render(request, 'tour/create-media-city.html', context)

@superuser_required(login_url='login')
def create_media_country(request, id):
    country = Country.objects.get(id=id)
    forms = CityCountryMediaForm()
    
    if request.method == 'POST':
        forms = CityCountryMediaForm(request.POST, request.FILES)
        
        if forms.is_valid():
            media = forms.save(commit=False)
            media.country = country
            media.save()
            
            messages.success(request, f'رسانه "{media.title}" با موفقیت اضافه شد.')
            return redirect('create-media-country', country.id)
    context = {
        'FormSet': forms,
        'country': country,
    }
    return render(request, 'tour/create-media-country.html', context)

@superuser_required(login_url='login')
def update_media_city(request, id):
    city_media = CityCountryMedia.objects.get(id=id)
    form = CityCountryMediaForm(instance=city_media)
    
    if request.method == 'POST':
        forms = CityCountryMediaForm(request.POST, request.FILES, instance=city_media)
        if forms.is_valid():
            forms.save()
            return redirect('create-media-city', city_media.city.id)
    
    context = {
        'FormSet': form,
        'city': city_media,
    }
    return render(request, 'tour/create-media-city.html', context)

@superuser_required(login_url='login')
def update_media_country(request, id):
    country_media = CityCountryMedia.objects.get(id=id)
    form = CityCountryMediaForm(instance=country_media)
    
    if request.method == 'POST':
        forms = CityCountryMediaForm(request.POST, request.FILES, instance=country_media)
        if forms.is_valid():
            forms.save()
            return redirect('create-media-country', country_media.country.id)
    
    context = {
        'FormSet': form,
        'country': country_media,
    }
    return render(request, 'tour/create-media-country.html', context)

@superuser_required(login_url='login')
def delete_media_city(request, id):
    media = CityCountryMedia.objects.get(id=id)
    city_id = media.city_id
    country_id = media.country_id
    media.delete()
    if city_id:
        return redirect('create-media-city', city_id)
    if country_id:
        return redirect('create-media-country', country_id)
    return redirect('city_list')

@superuser_required(login_url='login')
def delete_media_country(request, id):
    media = CityCountryMedia.objects.get(id=id)
    country_id = media.country_id
    media.delete()
    return redirect('create-media-country', country_id)

@superuser_required(login_url='login')
def city_list(request):
    return render(request, 'destinations/city_list.html')

def add_related_tour(request, id):
    tour = Tour.objects.get(id=id)
    countries = Country.objects.all()
    related_cities = related_tour_city.objects.filter(tour=tour)
    forms = relatedCityForm()
    if request.method == 'POST':
        forms = relatedCityForm(request.POST)
        if forms.is_valid():
            new_city = forms.save(commit=False)
            new_city.tour = tour
            new_city.save()
            return redirect('add_related_tour', tour.id)
    context = {
        'Tour': tour,
        'Form': forms,
        'Cities':related_cities,
        'countries': countries
    }
    return render(request, 'tour/add_related_city.html', context)

def update_related_tour(request, id):
    countries = Country.objects.all()
    related_tour = related_tour_city.objects.get(id=id)
    related_tours = related_tour_city.objects.filter(tour=related_tour.tour)
    forms = relatedCityForm(instance=related_tour)
    if request.method == 'POST':
        forms = relatedCityForm(request.POST, instance=related_tour)
        if forms.is_valid():
            new_city = forms.save(commit=False)
            new_city.save()
            return redirect('add_related_tour', related_tour.tour.id)
    context = {
        'Tour': related_tour.tour,
        'Form': forms,
        'tours': related_tours,
        'countries': countries,
        'related_tours': related_tour
    }
    return render(request, 'tour/add_related_city.html', context)

def delete_related_tour(request, id):
    related_cities = related_tour_city.objects.get(id=id)
    tour_id = related_cities.tour.id
    related_cities.delete()
    return redirect('add_related_tour', tour_id)

def related_city_ajax(request):
    country = request.GET.get('country')
    cities = City.objects.all()
    if country != '':
        cities = cities.filter(CountryName=country)
    context = {
        'cities': cities
    }
    return render(request, 'ajax/related-city-ajax.html', context)

def related_tour_ajax(request):
    city = request.GET.get('city')
    tours = Tour.objects.all()
    if city != '':
        tours = tours.filter(Tcity=city)
    context = {
        'tours': tours
    }
    return render(request, 'ajax/related-tour-ajax.html', context)
