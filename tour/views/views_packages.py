import json
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from tablib import Dataset

from hotels.models import Hotel_Data
from tour.pms_manager import *
from django.shortcuts import render, redirect
from django.contrib import messages
from tour.models import Package, MainPackage, Tour, TourCity, Currency
from tour.forms import CreatePackageForm, AddToPackageForm, CurrencyForm
from tour.resources import packages_resource, packages_import_resource


# Currency CURD Functions
@superuser_required(login_url='login')
def create_currency(request):
    allcry = Currency.objects.all()
    form = CurrencyForm()
    if request.method == 'POST':
        forms = CurrencyForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('create-currency')
        else:
            context = {
                'Data': allcry,
                'Form': forms,
            }
            return render(request, 'package/create-currency.html', context)
    context = {
        'Data': allcry,
        'Form': form
    }
    return render(request, 'package/create-currency.html', context)


@superuser_required(login_url='login')
def update_currency(request, id):
    allcry = Currency.objects.all()
    cry = Currency.objects.get(id=id)
    form = CurrencyForm(instance=cry)
    if request.method == 'POST':
        forms = CurrencyForm(request.POST, instance=cry)
        if forms.is_valid():
            forms.save()
            return redirect('create-currency')
        else:
            context = {
                'Data': allcry,
                'Form': forms,
            }
            return render(request, 'package/create-currency.html', context)
    context = {
        'Data': allcry,
        'Form': form
    }
    return render(request, 'package/create-currency.html', context)


@superuser_required(login_url='login')
def delete_currency(request, id):
    cry = Currency.objects.get(id=id)
    cry.delete()
    return redirect('create-currency')


# Main PAckage CRUD Functions
@superuser_required(login_url='login')
def create_package(request):
    forms = CreatePackageForm()
    user = request.user
    if request.method == 'POST':
        forms = CreatePackageForm(request.POST)
        if forms.is_valid():
            package_data = forms.save(commit=False)
            package_data.Creator = user
            package_data.save()
            messages.success(request, 'پکیج با موفقیت ثبت شد')
            return redirect('create-package')
        else:
            messages.error(request, 'برای ثبت اطلاعات تمام فیلدها باید تکمیل گردد')
            return redirect('create-package')
    context = {
        'form': forms
    }
    return render(request, 'package/create-package.html', context)


@superuser_required(login_url='login')
def update_main_packegs(request, id):
    mainpkg = MainPackage.objects.get(id=id)
    forms = CreatePackageForm(instance=mainpkg)
    if request.method == 'POST':
        forms = CreatePackageForm(request.POST, instance=mainpkg)
        if forms.is_valid():
            forms.save()
    context = {
        'form': forms
    }
    return render(request, 'package/create-package.html', context)


@superuser_required(login_url='login')
def delete_main_package(request, id):
    mainpkg = MainPackage.objects.get(id=id)
    mainpkg.delete()
    return redirect('create-package')


# Tour Package CRUD Functions
@superuser_required(login_url='login')
def add_to_package(request, id):
    forms = AddToPackageForm()
    tour = Tour.objects.get(id=id)
    cities = TourCity.objects.filter(TourName_id=tour.id)
    user = request.user
    hotel_1 = []
    hotel_2 = []
    hotel_3 = []
    hotel_4 = []
    hotel_5 = []
    if 'p_data_sub' in request.POST:
        if request.POST.get('hname'):
            hotel_1 = Hotel_Data.objects.filter(id=int(request.POST.get('hname'))).first()
        if request.POST.get('h2name'):
            hotel_2 = Hotel_Data.objects.filter(id=int(request.POST.get('h2name'))).first()
        if request.POST.get('h3name'):
            hotel_3 = Hotel_Data.objects.filter(id=int(request.POST.get('h3name'))).first()
        if request.POST.get('h4name'):
            hotel_4 = Hotel_Data.objects.filter(id=int(request.POST.get('h4name'))).first()
        if request.POST.get('h5name'):
            hotel_5 = Hotel_Data.objects.filter(id=int(request.POST.get('h5name'))).first()
        forms = AddToPackageForm(request.POST)
        if forms.is_valid():
            package_data = forms.save(commit=False)
            package_data.Creator = user
            package_data.TourName = tour
            if hotel_1:
                package_data.HotelName = hotel_1
            if hotel_2:
                package_data.Mhotel = hotel_2
            if hotel_3:
                package_data.M1hotel = hotel_3
            if hotel_4:
                package_data.M2hotel = hotel_4
            if hotel_5:
                package_data.M3hotel = hotel_5
            package_data.mhotel_sold_out = package_data.hotel_sold_out
            package_data.m1hotel_sold_out = package_data.hotel_sold_out
            package_data.m2hotel_sold_out = package_data.hotel_sold_out
            package_data.m3hotel_sold_out = package_data.hotel_sold_out
            package_data.save()
            cache.clear()
            return redirect('add-to-package', id=tour.id)
        else:
            messages.error(request, 'برای ثبت اطلاعات تمام فیلدها باید تکمیل گردد')
            context = {
                'form': forms,
                'Tour': tour,
                'Cities': cities,
            }
            return render(request, 'package/add-to-package.html', context)
            # return redirect('add-to-package', tour.id)
    if 'submit_file' in request.POST:
        package_resource = packages_import_resource()
        dataset = Dataset()
        packages_data = request.FILES['myfile']
        imported_data = dataset.load(packages_data.read())
        result = package_resource.import_data(dataset, dry_run=True, raise_errors=True)
        if not result.has_errors():
            package_resource.import_data(dataset, dry_run=False)  # Actually import now
            messages.success(request, 'اطلاعات پکیج با موفقیت ثبت شد')
            return redirect('add-to-package', tour.id)
        else:
            return redirect('add-to-package', tour.id)
    context = {
        'form': forms,
        'Tour': tour,
        'Cities': cities,
    }
    return render(request, 'package/add-to-package.html', context)

@superuser_required(login_url='login')
def toggle_tour_pub(request, id):
    tour = Tour.objects.get(id=id)
    if request.method == 'POST':
        tour.PubTour = not tour.PubTour
        tour.save(update_fields=['PubTour'])
        if tour.PubTour:
            messages.success(request, 'تور فعال شد و در سایت نمایش داده می‌شود')
        else:
            messages.success(request, 'تور غیرفعال شد و در سایت نمایش داده نمی‌شود')
    return redirect('add-to-package', id=tour.id)


@superuser_required(login_url='login')
def update_package(request, id):
    user = request.user
    package = Package.objects.get(id=id)
    tour = Tour.objects.get(id=package.TourName.id)
    cities = TourCity.objects.filter(TourName_id=tour.id)
    forms = AddToPackageForm(instance=package)
    hotel_1 = []
    hotel_2 = []
    hotel_3 = []
    hotel_4 = []
    hotel_5 = []
    if request.method == 'POST':
        forms = AddToPackageForm(request.POST, instance=package)
        if request.POST.get('hname'):
            hotel_1 = Hotel_Data.objects.filter(id=int(request.POST.get('hname'))).first()
        if request.POST.get('h2name'):
            hotel_2 = Hotel_Data.objects.filter(id=int(request.POST.get('h2name'))).first()
        if request.POST.get('h3name'):
            hotel_3 = Hotel_Data.objects.filter(id=int(request.POST.get('h3name'))).first()
        if request.POST.get('h4name'):
            hotel_4 = Hotel_Data.objects.filter(id=int(request.POST.get('h4name'))).first()
        if request.POST.get('h5name'):
            hotel_5 = Hotel_Data.objects.filter(id=int(request.POST.get('h5name'))).first()
        if forms.is_valid():
            package_data = forms.save(commit=False)
            package_data.Creator = user
            if hotel_1:
                package_data.HotelName = hotel_1
            if hotel_2:
                package_data.Mhotel = hotel_2
            if hotel_3:
                package_data.M1hotel = hotel_3
            if hotel_4:
                package_data.M2hotel = hotel_4
            if hotel_5:
                package_data.M3hotel = hotel_5
            package_data.mhotel_sold_out = package_data.hotel_sold_out
            package_data.m1hotel_sold_out = package_data.hotel_sold_out
            package_data.m2hotel_sold_out = package_data.hotel_sold_out
            package_data.m3hotel_sold_out = package_data.hotel_sold_out
            package_data.save()
            cache.clear()
            return redirect('add-to-package', id=package.TourName.id)
        else:
            messages.error(request, 'برای ثبت اطلاعات تمام فیلدها باید تکمیل گردد')
            return redirect('add-to-package', id=package.TourName.id)
    context = {
        'form': forms,
        'Tour': tour,
        'Cities': cities,
        'package': package
    }
    return render(request, 'package/add-to-package.html', context)


@superuser_required(login_url='login')
def delete_package(request, id):
    package = Package.objects.get(id=id)
    tour_id = package.TourName.id
    date_plan_id = package.exclusive_date_plan_id
    package.delete()
    cache.clear()
    if date_plan_id:
        return redirect('tour_date_plan_hotel_prices', id=date_plan_id)
    return redirect('add-to-package', id=tour_id)


@superuser_required(login_url='login')
def packages(request):
    tour_id = request.GET.get('tour_id')
    date_plan_id = request.GET.get('date_plan_id')
    if date_plan_id:
        all_packages = Package.objects.filter(
            TourName_id=tour_id, exclusive_date_plan_id=date_plan_id
        ).order_by('DoubleBedPrice_doller')
    else:
        all_packages = Package.objects.filter(
            TourName_id=tour_id, exclusive_date_plan__isnull=True
        ).order_by('DoubleBedPrice_doller')
    main_packages = MainPackage.objects.all()
    all_currency = Currency.objects.all()
    context = {
        'AllData': all_packages,
        'main_packages': main_packages,
        'all_currency': all_currency
    }
    return render(request, 'package/packages.html', context)


@superuser_required(login_url='login')
def package_hotel_list(request):
    hotels = Hotel_Data.objects.select_related('Hcity').only('HotelName', 'Hcity__Name', 'id')
    return render(request, 'package/hotel_list.html', {'hotels': hotels})


@superuser_required(login_url='login')
def export_tour_packages(request):
    tour_id = int(request.GET.get('id'))
    query_set = Package.objects.filter(TourName=tour_id).order_by('DoubleBedPrice')
    package_res = packages_resource()
    data = package_res.export(query_set)
    response = HttpResponse(data.xlsx, content_type='text/xlsx')
    response['Content-Disposition'] = f'attachment; filename="{tour_id}.xlsx"'
    return response


@superuser_required(login_url='login')
def import_tour_packages(request):
    tour_id = int(request.GET.get('id'))
    query_set = Package.objects.filter(TourName=tour_id).order_by('DoubleBedPrice')
    package_res = packages_resource()
    data = package_res.export(query_set)
    response = HttpResponse(data.xls, content_type='text/xls')
    response['Content-Disposition'] = f'attachment; filename="{tour_id}.xls"'
    return response


@superuser_required(login_url='login')
def change_price_selected_package(request):
    packages_list = request.GET.get('packages')
    double = request.GET.get('double')
    singel = request.GET.get('singel')
    bwb_price = request.GET.get('bwb_price')
    bwob_price = request.GET.get('bwob_price')
    infont_price = request.GET.get('infont_price')
    for i in json.loads(packages_list):
        package = Package.objects.get(id=i)
        package.DoubleBedPrice += int(double)
        package.SingleBedPrice += int(singel)
        package.BabyWithBedPrice += int(bwb_price)
        package.BabyWithoutBedPrice += int(bwob_price)
        package.BabyWithoutBedPrice += int(bwob_price)
        package.InfontPrice += int(infont_price)
        package.save()
    cache.clear()
    return JsonResponse(
        {
            'status': 'ok',
            'packages_list': packages_list,
        }
    )

def change_package_price_single(request):
    package_id = request.GET.get('package_id')
    package = Package.objects.get(id=package_id)
    hotel1 = request.GET.get('hotel1')
    if hotel1:
        hotel1 = Hotel_Data.objects.get(id=hotel1)
        package.HotelName = hotel1
    hotel1_view = request.GET.get('hotel1_view')
    hotel1_service = request.GET.get('hotel1_service')
    if hotel1_view:
        package.view_hotel = hotel1_view
    else:
        package.view_hotel = None
    if hotel1_service:
        package.service_hotel = hotel1_service
    else:
        package.service_hotel = None
    hotel2 = request.GET.get('hotel2')
    if hotel2:
        hotel2 = Hotel_Data.objects.get(id=hotel2)
        package.Mhotel = hotel2
    else:
        package.Mhotel = None
    hotel2_view = request.GET.get('hotel2_view')
    hotel2_service = request.GET.get('hotel2_service')
    if hotel2_view:
        package.view_mhotel = hotel2_view
    else:
        package.view_mhotel = None
    if hotel2_service:
        package.service_mhotel = hotel2_service
    else:
        package.service_mhotel = None
    hotel3 = request.GET.get('hotel3')
    if hotel3:
        hotel3 = Hotel_Data.objects.get(id=hotel3)
        package.M1hotel = hotel3
    else:
        package.M1hotel = None
    hotel3_view = request.GET.get('hotel3_view')
    hotel3_service = request.GET.get('hotel3_service')
    if hotel3_view:
        package.view_m1hotel = hotel3_view
    else:
        package.view_m1hotel = None
    if hotel3_service:
        package.service_m1hotel = hotel3_service
    else:
        package.service_m1hotel = None
    hotel4 = request.GET.get('hotel4')
    if hotel4:
        hotel4 = Hotel_Data.objects.get(id=hotel4)
        package.M2hotel = hotel4
    else:
        package.M2hotel = None
    hotel4_view = request.GET.get('hotel4_view')
    hotel4_service = request.GET.get('hotel4_service')
    if hotel4_view:
        package.view_m2hotel = hotel4_view
    else:
        package.view_m2hotel = None
    if hotel4_service:
        package.service_m2hotel = hotel4_service
    else:
        package.service_m2hotel = None
    hotel5 = request.GET.get('hotel5')
    if hotel5:
        hotel5 = Hotel_Data.objects.get(id=hotel5)
        package.M3hotel = hotel5
    else:
        package.M3hotel = None
    hotel5_view = request.GET.get('hotel5_view')
    hotel5_service = request.GET.get('hotel5_service')
    if hotel5_view:
        package.view_m3hotel = hotel5_view
    else:
        package.view_m3hotel = None
    if hotel5_service:
        package.service_m3hotel = hotel5_service
    else:
        package.service_m3hotel = None
    mainpackages = request.GET.get('mainpackages')
    if mainpackages:
        mainpackages = MainPackage.objects.get(id=int(mainpackages))
    prcy = request.GET.get('prcy')
    if prcy:
        prcy = Currency.objects.get(id=int(prcy))
    fr_Pcry = request.GET.get('fr_Pcry')
    if fr_Pcry:
        fr_Pcry = Currency.objects.get(id=int(fr_Pcry))
        package.fr_Pcry = fr_Pcry
    if fr_Pcry == '':
        package.fr_Pcry = None
    main_view = request.GET.get('main_view')
    d_price = int(request.GET.get('d_price'))
    s_price = int(request.GET.get('s_price'))
    bwb_price = int(request.GET.get('bwb_price'))
    bwob_price = int(request.GET.get('bwob_price'))
    infont_price = int(request.GET.get('infont_price'))
    d_price_d = int(request.GET.get('d_price_d'))
    s_price_d = int(request.GET.get('s_price_d'))
    bwb_price_d = int(request.GET.get('bwb_price_d'))
    bwob_price_d = int(request.GET.get('bwob_price_d'))
    infonr_price_d = int(request.GET.get('infont_price_d'))
    package.DoubleBedPrice = int(d_price)
    package.SingleBedPrice = int(s_price)
    package.BabyWithBedPrice = int(bwb_price)
    package.BabyWithoutBedPrice = int(bwob_price)
    package.InfontPrice = int(infont_price)
    package.DoubleBedPrice_doller = int(d_price_d)
    package.SingleBedPrice_doller = int(s_price_d)
    package.BabyWithBedPrice_doller = int(bwb_price_d)
    package.BabyWithoutBedPrice_doller = int(bwob_price_d)
    package.InfontPrice_doller = int(infonr_price_d)
    package.DollerPrice = request.GET.get('static_price_d')
    package.Pcry = prcy
    package.MainPkg = mainpackages
    package.view = main_view
    soldout = request.GET.get('soldout') == 'true'
    package.hotel_sold_out = soldout
    package.mhotel_sold_out = soldout
    package.m1hotel_sold_out = soldout
    package.m2hotel_sold_out = soldout
    package.m3hotel_sold_out = soldout
    package.save()
    cache.clear()
    return JsonResponse(
        {
            'stutus': 'changed!'
        }
    )
