from django.contrib.auth.decorators import user_passes_test
from datetime import datetime
from django.core.cache import cache
from django.shortcuts import render, redirect
from tour.forms import CreateTourForm, tour_search_form, _parse_amount
from django.contrib import messages
from tour.models import Tour, Package, TourCity,\
    tour_images, related_tour_city, date_plan, DatePlanPackagePrice, ApiPartner, Country, City,\
    MainPackage, Currency, SERVICE

from tour.forms import TourCityForm, tour_date_form, ApiPartnerForm, AddToPackageForm


def superuser_required(login_url=None):
    return user_passes_test(lambda u: u.is_superuser or hasattr(u, 'staff_access'), login_url=login_url)


@superuser_required(login_url='login')
def create_tour(request):
    date = datetime.now()
    form = CreateTourForm()
    user = request.user

    if request.method == 'POST':
        form = CreateTourForm(request.POST, request.FILES)

        if form.is_valid():
            tour = form.save(commit=False)
            tour.Creator = user
            tour.updateDate = date
            tour.save()

            form.save_m2m()

            for cat in tour.custom_categories.all():
                if tour.Tcity:
                    cat.cities.add(tour.Tcity)
                if tour.Tcountry:
                    cat.countries.add(tour.Tcountry)

            related_tour_city.objects.create(
                country=tour.Tcountry,
                city=tour.Tcity,
                tour=tour
            )

            files = request.FILES.getlist('files')
            for file in files:
                tour_images.objects.create(tour=tour, image=file)

            return redirect('tour_date_plan', pk=tour.id)

        messages.error(request, 'لطفا تمام فیلدها را تکمیل نمایید')

    return render(request, 'tour/create-tour.html', {'form': form})

@superuser_required(login_url='login')
def update_tour(request, id):
    date = datetime.now()
    tour = Tour.objects.get(id=id)
    galley = tour_images.objects.filter(tour=tour)

    form = CreateTourForm(instance=tour)

    if request.method == 'POST':
        old_categories = set(tour.custom_categories.all())
        richtext_fields = ['ShortDsc', 'documents', 'Description', 'cancel_policy', 'about_tour']
        previous_richtext = {f: getattr(tour, f) for f in richtext_fields if hasattr(tour, f)}
        form = CreateTourForm(request.POST, request.FILES, instance=tour)

        if form.is_valid():
            t = form.save(commit=False)
            t.updateDate = date
            # for field_name in previous_richtext:
            #     submitted_value = (getattr(t, field_name) or '').strip()
            #     if not submitted_value and previous_richtext[field_name]:
            #         setattr(t, field_name, previous_richtext[field_name])
            for field_name in previous_richtext:
                submitted_value = (getattr(t, field_name) or '').strip()
                touched = request.POST.get(field_name + '_touched') == '1'
                if not submitted_value and previous_richtext[field_name] and not touched:
                    setattr(t, field_name, previous_richtext[field_name])

            t.save()

            form.save_m2m()
            
            new_categories = set(t.custom_categories.all())
            all_categories = old_categories.union(new_categories)
            
            for cat in all_categories:
                cat.sync_locations()

            packages = Package.objects.filter(TourName=t.id)
            for i in packages:
                i.SingleBedPrice += t.add_peice_single
                i.DoubleBedPrice += t.add_peice_dubel
                i.BabyWithBedPrice += t.add_peice_with_bed
                i.BabyWithoutBedPrice += t.add_peice_without_bed
                i.InfontPrice += t.add_peice_infont
                i.save()

            t.add_peice_dubel = 0
            t.add_peice_single = 0
            t.add_peice_with_bed = 0
            t.add_peice_without_bed = 0
            t.add_peice_infont = 0
            t.save()

            files = request.FILES.getlist('files')
            for file in files:
                tour_images.objects.create(tour=t, image=file)

            return redirect('tour_date_plan', pk=t.id)

    return render(request, 'tour/create-tour.html', {
        'form': form,
        'Data': tour,
        'galley': galley
    })

@superuser_required(login_url='login')
def delete_tour(request, id):
    tour = Tour.objects.get(id=id)
    tour.delete()
    return redirect('tour-list')


@superuser_required(login_url='login')
def tour_list(request):
    forms = tour_search_form()
    context = {
        'forms': forms
    }
    return render(request, 'tour/list.html', context)


@superuser_required(login_url='login')
def add_city_tour(request, pk):
    tour = Tour.objects.get(id=pk)
    cities = TourCity.objects.filter(TourName_id=tour.id)
    form = TourCityForm()
    if request.method == 'POST':
        forms = TourCityForm(request.POST)
        if forms.is_valid():
            city = forms.save(commit=False)
            city.TourName = tour
            city.save()
            context = {
                'Tour': tour,
                'Cities': cities,
                'Form': form
            }
            return render(request, 'tour/tour-city-list.html', context)
    context = {
        'Tour': tour,
        'Cities': cities,
        'Form': form
    }
    return render(request, 'tour/tour-city-list.html', context)


@superuser_required(login_url='login')
def update_city_tour(request, id):
    city = TourCity.objects.get(id=id)
    tour = Tour.objects.get(id=city.TourName_id)
    nid = tour.id
    cities = TourCity.objects.filter(TourName_id=tour.id)
    form = TourCityForm(instance=city)
    if request.method == 'POST':
        forms = TourCityForm(request.POST, instance=city)
        if forms.is_valid():
            city = forms.save(commit=False)
            city.TourName = tour
            city.save()
            context = {
                'Tour': tour,
                'Cities': cities,
                'Form': form
            }
            return redirect('tour-city-list', pk=nid)
    context = {
        'Tour': tour,
        'Cities': cities,
        'Form': form
    }
    return render(request, 'tour/tour-city-list.html', context)


@superuser_required(login_url='login')
def delete_city_tour(request, id):
    city = TourCity.objects.get(id=id)
    tour = Tour.objects.get(id=city.TourName_id)
    nid = tour.id
    city.delete()
    return redirect('tour-city-list', pk=nid)


def _tour_price_currencies(tour):
    pkg = Package.objects.filter(TourName=tour).order_by('DoubleBedPrice', 'DoubleBedPrice_doller').first()
    main_currency = str(pkg.Pcry) if pkg and pkg.Pcry else 'تومان'
    foreign_currency = str(pkg.fr_Pcry) if pkg and pkg.fr_Pcry else 'دلار'
    return main_currency, foreign_currency


@superuser_required(login_url='login')
def tour_date_plan(request, pk):
    tour = Tour.objects.get(id=pk)
    dates = date_plan.objects.filter(tour_id=tour.id).order_by('start_date')
    main_currency, foreign_currency = _tour_price_currencies(tour)
    form = tour_date_form()
    if request.method == 'POST':
        forms = tour_date_form(request.POST)
        if forms.is_valid():
            new_date = forms.save(commit=False)
            new_date.tour = tour
            new_date.save()
            dates = date_plan.objects.filter(tour_id=tour.id).order_by('start_date')
            context = {
                'Tour': tour,
                'Dates': dates,
                'Form': form,
                'main_currency': main_currency,
                'foreign_currency': foreign_currency,
            }
            return render(request, 'tour/tour-date-list.html', context)
    context = {
        'Tour': tour,
        'Dates': dates,
        'Form': form,
        'main_currency': main_currency,
        'foreign_currency': foreign_currency,
    }
    return render(request, 'tour/tour-date-list.html', context)


@superuser_required(login_url='login')
def tour_date_plan_update(request, id):
    date_item = date_plan.objects.get(id=id)
    tour = Tour.objects.get(id=date_item.tour.id)
    dates = date_plan.objects.filter(tour_id=tour.id).order_by('start_date')
    main_currency, foreign_currency = _tour_price_currencies(tour)
    form = tour_date_form(instance=date_item)
    if request.method == 'POST':
        forms = tour_date_form(request.POST, instance=date_item)
        if forms.is_valid():
            new_date = forms.save(commit=False)
            new_date.tour = tour
            new_date.save()
            return redirect('tour_date_plan', tour.id)
    context = {
        'Tour': tour,
        'Dates': dates,
        'Form': form,
        'main_currency': main_currency,
        'foreign_currency': foreign_currency,
    }
    return render(request, 'tour/tour-date-list.html', context)

@superuser_required(login_url='login')
def tour_date_plan_delete(request, id):
    date_item = date_plan.objects.get(id=id)
    tour_id = date_item.tour.id
    date_item.delete()
    return redirect('tour_date_plan', tour_id)


def _date_plan_default_prices(date_item, pkg):
    """قیمت هر هتل برای این تاریخ در صورتی که قیمت دستی ثبت نشده باشد (طبق اختلاف قیمت یکسان تاریخ)."""
    dollar_type = date_item.price_dollar_type if date_item.price_dollar_type in ('افزایش', 'کاهش') else date_item.price_type
    sign = 1 if date_item.price_type == 'افزایش' else -1 if date_item.price_type == 'کاهش' else 0
    sign_f = 1 if dollar_type == 'افزایش' else -1 if dollar_type == 'کاهش' else 0
    adj = int(date_item.price or 0)
    adj_foreign = int(date_item.price_dollar or 0)
    adj_infant = int(date_item.infant_price or 0)
    adj_infant_foreign = int(date_item.infant_price_dollar or 0)
    return {
        'DoubleBedPrice': (pkg.DoubleBedPrice or 0) + sign * adj,
        'SingleBedPrice': (pkg.SingleBedPrice or 0) + sign * adj,
        'BabyWithBedPrice': (pkg.BabyWithBedPrice or 0) + sign * adj,
        'BabyWithoutBedPrice': (pkg.BabyWithoutBedPrice or 0) + sign * adj,
        'InfontPrice': (pkg.InfontPrice or 0) + sign * adj_infant,
        'DoubleBedPrice_doller': (pkg.DoubleBedPrice_doller or 0) + sign_f * adj_foreign,
        'SingleBedPrice_doller': (pkg.SingleBedPrice_doller or 0) + sign_f * adj_foreign,
        'BabyWithBedPrice_doller': (pkg.BabyWithBedPrice_doller or 0) + sign_f * adj_foreign,
        'BabyWithoutBedPrice_doller': (pkg.BabyWithoutBedPrice_doller or 0) + sign_f * adj_foreign,
        'InfontPrice_doller': (pkg.InfontPrice_doller or 0) + sign_f * adj_infant_foreign,
    }


_DATE_PLAN_PRICE_FIELDS = [
    'DoubleBedPrice', 'SingleBedPrice', 'BabyWithBedPrice', 'BabyWithoutBedPrice', 'InfontPrice',
    'DoubleBedPrice_doller', 'SingleBedPrice_doller', 'BabyWithBedPrice_doller', 'BabyWithoutBedPrice_doller',
    'InfontPrice_doller',
]

_DATE_PLAN_PRICE_POST_KEYS = {
    'DoubleBedPrice': 'double',
    'SingleBedPrice': 'single',
    'BabyWithBedPrice': 'bwb',
    'BabyWithoutBedPrice': 'bwob',
    'InfontPrice': 'infant',
    'DoubleBedPrice_doller': 'double_d',
    'SingleBedPrice_doller': 'single_d',
    'BabyWithBedPrice_doller': 'bwb_d',
    'BabyWithoutBedPrice_doller': 'bwob_d',
    'InfontPrice_doller': 'infant_d',
}

_SOLDOUT_SLOTS = [
    ('hotel_sold_out', 'HotelName'),
    ('mhotel_sold_out', 'Mhotel'),
    ('m1hotel_sold_out', 'M1hotel'),
    ('m2hotel_sold_out', 'M2hotel'),
    ('m3hotel_sold_out', 'M3hotel'),
]

_HOTEL_SLOTS = [
    # (hotel_attr, hotel_override_field, hotel_post_key, view_field, service_field, view_post_key, service_post_key)
    ('HotelName', 'hotel_override', 'hotelslot0', 'view_hotel', 'service_hotel', 'viewslot0', 'serviceslot0'),
    ('Mhotel', 'mhotel_override', 'hotelslot1', 'view_mhotel', 'service_mhotel', 'viewslot1', 'serviceslot1'),
    ('M1hotel', 'm1hotel_override', 'hotelslot2', 'view_m1hotel', 'service_m1hotel', 'viewslot2', 'serviceslot2'),
    ('M2hotel', 'm2hotel_override', 'hotelslot3', 'view_m2hotel', 'service_m2hotel', 'viewslot3', 'serviceslot3'),
    ('M3hotel', 'm3hotel_override', 'hotelslot4', 'view_m3hotel', 'service_m3hotel', 'viewslot4', 'serviceslot4'),
]



@superuser_required(login_url='login')
def tour_date_plan_hotel_prices(request, id):
    date_item = date_plan.objects.select_related('tour').get(id=id)
    tour = date_item.tour
    main_currency, foreign_currency = _tour_price_currencies(tour)
    # پکیج‌های مخصوص این تاریخ جدا مدیریت می‌شوند (بخش «پکیج‌های مخصوص این تاریخ» پایین‌تر)
    # و اینجا تکراری نمایش داده نمی‌شوند
    packages = Package.objects.filter(TourName=tour, exclusive_date_plan__isnull=True).select_related(
        'HotelName', 'Mhotel', 'M1hotel', 'M2hotel', 'M3hotel'
    ).order_by('DoubleBedPrice', 'DoubleBedPrice_doller')
    exclusive_packages = Package.objects.filter(
        TourName=tour, exclusive_date_plan=date_item
    ).select_related('HotelName', 'Mhotel', 'M1hotel', 'M2hotel', 'M3hotel').order_by('DoubleBedPrice', 'DoubleBedPrice_doller')
    overrides = {o.package_id: o for o in DatePlanPackagePrice.objects.filter(date_plan=date_item)}

    if 'add_package_sub' in request.POST:
        add_form = AddToPackageForm(request.POST)
        hotel1_id = request.POST.get('add_hotel1')
        if add_form.is_valid() and hotel1_id:
            new_pkg = add_form.save(commit=False)
            new_pkg.Creator = request.user
            new_pkg.TourName = tour
            new_pkg.exclusive_date_plan = date_item
            new_pkg.HotelName_id = int(hotel1_id)
            for post_name, attr in [
                ('add_hotel2', 'Mhotel'), ('add_hotel3', 'M1hotel'),
                ('add_hotel4', 'M2hotel'), ('add_hotel5', 'M3hotel'),
            ]:
                raw_value = request.POST.get(post_name)
                setattr(new_pkg, f'{attr}_id', int(raw_value) if raw_value else None)
            new_pkg.mhotel_sold_out = new_pkg.hotel_sold_out
            new_pkg.m1hotel_sold_out = new_pkg.hotel_sold_out
            new_pkg.m2hotel_sold_out = new_pkg.hotel_sold_out
            new_pkg.m3hotel_sold_out = new_pkg.hotel_sold_out
            new_pkg.save()
            cache.clear()
            messages.success(request, 'پکیج مخصوص این تاریخ با موفقیت اضافه شد')
        else:
            messages.error(request, 'برای افزودن پکیج، حداقل انتخاب هتل اول و تکمیل فیلدهای الزامی لازم است')
        return redirect('tour_date_plan_hotel_prices', id=date_item.id)

    if request.method == 'POST':
        for pkg in packages:
            assigned_fields = [field for field, hotel_attr in _SOLDOUT_SLOTS if getattr(pkg, hotel_attr)]
            hotel_slots = [slot for slot in _HOTEL_SLOTS if getattr(pkg, slot[0])]
            defaults = _date_plan_default_prices(date_item, pkg)
            submitted = {
                field: _parse_amount(request.POST.get(f'{post_key}_{pkg.id}'))
                for field, post_key in _DATE_PLAN_PRICE_POST_KEYS.items()
            }
            soldout_defaults = {field: getattr(pkg, field) for field in assigned_fields}
            soldout_submitted_value = bool(request.POST.get(f'soldout_{pkg.id}'))
            soldout_submitted = {field: soldout_submitted_value for field in assigned_fields}
            hidden_submitted = bool(request.POST.get(f'hidden_{pkg.id}'))
            hotel_override_submitted = {}
            view_service_submitted = {}
            view_service_defaults = {}
            for hotel_attr, override_field, post_key, view_field, service_field, view_key, service_key in hotel_slots:
                raw_value = request.POST.get(f'{post_key}_{pkg.id}')
                submitted_id = int(raw_value) if raw_value else None
                base_hotel_id = getattr(pkg, f'{hotel_attr}_id')
                # اگه همون هتل پیش‌فرض دوباره انتخاب شده باشه، یعنی جایگزینی واقعی نیست
                hotel_override_submitted[override_field] = None if submitted_id == base_hotel_id else submitted_id
                view_service_submitted[view_field] = request.POST.get(f'{view_key}_{pkg.id}') or ''
                view_service_submitted[service_field] = request.POST.get(f'{service_key}_{pkg.id}') or ''
                view_service_defaults[view_field] = getattr(pkg, view_field) or ''
                view_service_defaults[service_field] = getattr(pkg, service_field) or ''
            mainpkg_raw = request.POST.get(f'mainpkg_{pkg.id}')
            currency_raw = request.POST.get(f'currency_{pkg.id}')
            fcurrency_raw = request.POST.get(f'fcurrency_{pkg.id}')
            pkgview_submitted = request.POST.get(f'pkgview_{pkg.id}') or ''
            dollerprice_submitted = request.POST.get(f'dollerprice_{pkg.id}') or ''
            mainpkg_submitted = int(mainpkg_raw) if mainpkg_raw else None
            currency_submitted = int(currency_raw) if currency_raw else None
            fcurrency_submitted = int(fcurrency_raw) if fcurrency_raw else None
            existing = overrides.get(pkg.id)
            prices_match_default = all(submitted[field] == defaults[field] for field in _DATE_PLAN_PRICE_FIELDS)
            soldout_matches_default = all(
                soldout_submitted[field] == soldout_defaults[field] for field in assigned_fields
            )
            hidden_matches_default = hidden_submitted is False
            hotel_override_matches_default = all(value is None for value in hotel_override_submitted.values())
            view_service_matches_default = all(
                view_service_submitted[field] == view_service_defaults[field] for field in view_service_defaults
            )
            meta_matches_default = (
                mainpkg_submitted == pkg.MainPkg_id
                and currency_submitted == pkg.Pcry_id
                and fcurrency_submitted == pkg.fr_Pcry_id
                and pkgview_submitted == (pkg.view or '')
                and dollerprice_submitted == (pkg.DollerPrice or '')
            )
            if (prices_match_default and soldout_matches_default and hidden_matches_default
                    and hotel_override_matches_default and view_service_matches_default and meta_matches_default):
                if existing:
                    existing.delete()
                continue
            override = existing or DatePlanPackagePrice(date_plan=date_item, package=pkg)
            for field, value in submitted.items():
                setattr(override, field, value)
            for field, value in soldout_submitted.items():
                setattr(override, field, value)
            override.is_hidden = hidden_submitted
            for field, value in hotel_override_submitted.items():
                setattr(override, f'{field}_id', value)
            for field, value in view_service_submitted.items():
                setattr(override, field, value or None)
            override.main_pkg_id = mainpkg_submitted
            override.currency_id = currency_submitted
            override.foreign_currency_id = fcurrency_submitted
            override.view = pkgview_submitted or None
            override.doller_price = dollerprice_submitted or None
            override.save()

        # پکیج‌های مخصوص این تاریخ فقط برای همین تاریخ وجود دارن، پس اینجا override
        # نمی‌سازیم و مستقیم روی خودِ پکیج ذخیره می‌کنیم
        for pkg in exclusive_packages:
            if request.POST.get(f'deletepkg_{pkg.id}'):
                pkg.delete()
                continue
            hotel_slots = [slot for slot in _HOTEL_SLOTS if getattr(pkg, slot[0])]
            for field, post_key in _DATE_PLAN_PRICE_POST_KEYS.items():
                setattr(pkg, field, _parse_amount(request.POST.get(f'{post_key}_{pkg.id}')))
            for hotel_attr, override_field, post_key, view_field, service_field, view_key, service_key in hotel_slots:
                raw_hotel = request.POST.get(f'{post_key}_{pkg.id}')
                if raw_hotel:
                    setattr(pkg, f'{hotel_attr}_id', int(raw_hotel))
                setattr(pkg, view_field, request.POST.get(f'{view_key}_{pkg.id}') or None)
                setattr(pkg, service_field, request.POST.get(f'{service_key}_{pkg.id}') or None)
            mainpkg_raw = request.POST.get(f'mainpkg_{pkg.id}')
            currency_raw = request.POST.get(f'currency_{pkg.id}')
            fcurrency_raw = request.POST.get(f'fcurrency_{pkg.id}')
            if mainpkg_raw:
                pkg.MainPkg_id = int(mainpkg_raw)
            pkg.Pcry_id = int(currency_raw) if currency_raw else None
            pkg.fr_Pcry_id = int(fcurrency_raw) if fcurrency_raw else None
            pkg.view = request.POST.get(f'pkgview_{pkg.id}') or None
            pkg.DollerPrice = request.POST.get(f'dollerprice_{pkg.id}') or None
            soldout_value = bool(request.POST.get(f'soldout_{pkg.id}'))
            pkg.hotel_sold_out = soldout_value
            pkg.mhotel_sold_out = soldout_value
            pkg.m1hotel_sold_out = soldout_value
            pkg.m2hotel_sold_out = soldout_value
            pkg.m3hotel_sold_out = soldout_value
            pkg.save()

        cache.clear()
        messages.success(request, 'قیمت، هتل‌ها و وضعیت ظرفیت برای این تاریخ ذخیره شد')
        return redirect('tour_date_plan_hotel_prices', id=date_item.id)

    rows = []
    for pkg in packages:
        defaults = _date_plan_default_prices(date_item, pkg)
        override = overrides.get(pkg.id)
        assigned_fields = [field for field, hotel_attr in _SOLDOUT_SLOTS if getattr(pkg, hotel_attr)]
        is_sold_out = bool(assigned_fields) and all(
            (getattr(override, field) if override else getattr(pkg, field)) for field in assigned_fields
        )
        default_sold_out = bool(assigned_fields) and all(getattr(pkg, field) for field in assigned_fields)
        hotel_slots = []
        for hotel_attr, override_field, post_key, view_field, service_field, view_key, service_key in _HOTEL_SLOTS:
            base_hotel = getattr(pkg, hotel_attr)
            if not base_hotel:
                continue
            override_hotel = getattr(override, override_field) if override else None
            current_view = (getattr(override, view_field) if override and getattr(override, view_field) else None) or getattr(pkg, view_field)
            current_service = (getattr(override, service_field) if override and getattr(override, service_field) else None) or getattr(pkg, service_field)
            hotel_slots.append({
                'post_key': post_key,
                'view_post_key': view_key,
                'service_post_key': service_key,
                'base_hotel': base_hotel,
                'current_hotel': override_hotel or base_hotel,
                'is_overridden': override_hotel is not None,
                'current_view': current_view,
                'current_service': current_service,
            })
        meta = {
            'mainpkg_id': (override.main_pkg_id if override and override.main_pkg_id else pkg.MainPkg_id),
            'currency_id': (override.currency_id if override and override.currency_id else pkg.Pcry_id),
            'fcurrency_id': (override.foreign_currency_id if override and override.foreign_currency_id else pkg.fr_Pcry_id),
            'view': (override.view if override and override.view else pkg.view),
            'doller_price': (override.doller_price if override and override.doller_price else pkg.DollerPrice),
        }
        rows.append({
            'pkg': pkg,
            'is_override': override is not None,
            'values': {
                field: (getattr(override, field) if override else defaults[field])
                for field in _DATE_PLAN_PRICE_FIELDS
            },
            'defaults': defaults,
            'is_sold_out': is_sold_out,
            'default_sold_out': default_sold_out,
            'is_hidden': override.is_hidden if override else False,
            'hotel_slots': hotel_slots,
            'meta': meta,
        })

    for pkg in exclusive_packages:
        hotel_slots = []
        for hotel_attr, override_field, post_key, view_field, service_field, view_key, service_key in _HOTEL_SLOTS:
            base_hotel = getattr(pkg, hotel_attr)
            if not base_hotel:
                continue
            hotel_slots.append({
                'post_key': post_key,
                'view_post_key': view_key,
                'service_post_key': service_key,
                'base_hotel': base_hotel,
                'current_hotel': base_hotel,
                'is_overridden': False,
                'current_view': getattr(pkg, view_field),
                'current_service': getattr(pkg, service_field),
            })
        pkg.hotel_slots = hotel_slots
        pkg.meta = {
            'mainpkg_id': pkg.MainPkg_id,
            'currency_id': pkg.Pcry_id,
            'fcurrency_id': pkg.fr_Pcry_id,
            'view': pkg.view,
            'doller_price': pkg.DollerPrice,
        }
        pkg.values = {field: getattr(pkg, field) for field in _DATE_PLAN_PRICE_FIELDS}

    context = {
        'Tour': tour,
        'DateItem': date_item,
        'Rows': rows,
        'has_override': any(row['is_override'] for row in rows),
        'main_currency': main_currency,
        'foreign_currency': foreign_currency,
        'add_form': AddToPackageForm(),
        'exclusive_packages': exclusive_packages,
        'main_packages': MainPackage.objects.all(),
        'all_currency': Currency.objects.all(),
        'service_choices': [code for code, _ in SERVICE],
    }
    return render(request, 'tour/tour-date-hotel-prices.html', context)


@superuser_required(login_url='login')
def copy_tour_data(request, id):
    main_tour = Tour.objects.get(id=id)
    tour = Tour.objects.get(id=id)
    tour.Title = tour.Title + '(کپی)'
    tour.Slug = tour.Slug + '_copy'
    tour.PubTour = False
    tour.id = None
    tour.viewCount = 0
    tour.save()
    print(tour.id)
    cities = TourCity.objects.filter(TourName=main_tour)
    for i in cities:
        i.id = None
        i.TourName = tour
        i.save()
    pakcages = Package.objects.filter(TourName=main_tour)
    for i in pakcages:
        i.id = None
        i.TourName = tour
        i.save()
    return redirect('tour-list')

@superuser_required(login_url='login')
def remove_tour_gallery(request, id):
    item = tour_images.objects.get(id=id)
    tour = Tour.objects.get(id=item.tour.id)
    item.delete()
    return redirect('update-tour', tour.id)

@superuser_required(login_url='login')
def remove_tour_featured_image(request, id):
    tour = Tour.objects.get(id=id)
    tour.TourImage = ''
    tour.save()
    return redirect('update-tour', tour.id)

@superuser_required(login_url='login')
def remove_tour_main_image(request, id):
    tour = Tour.objects.get(id=id)
    tour.tour_main = ''
    tour.save()
    return redirect('update-tour', tour.id)

@superuser_required(login_url='login')
def remove_tour_pdf(request, id):
    tour = Tour.objects.get(id=id)
    tour.TourPdf = ''
    tour.save()
    return redirect('update-tour', tour.id)

@superuser_required(login_url='login')
def api_partner_list(request):
    partners = ApiPartner.objects.all().order_by('-created_at')
    editing_partner = None
    edit_id = request.GET.get('edit')
    if edit_id:
        editing_partner = ApiPartner.objects.filter(id=edit_id).first()

    if request.method == 'POST':
        partner_id = request.POST.get('partner_id')
        instance = ApiPartner.objects.filter(id=partner_id).first() if partner_id else None
        form = ApiPartnerForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('api-partner-list')
    else:
        form = ApiPartnerForm(instance=editing_partner)

    context = {
        'Partners': partners,
        'Form': form,
        'EditingPartner': editing_partner,
        'feed_base_url': request.build_absolute_uri('/api/tours/'),
        'countries': Country.objects.all().order_by('TitleC'),
        'cities': City.objects.all().order_by('Name'),
        'tours': Tour.objects.filter(PubTour=True).order_by('Title'),
    }
    return render(request, 'tour/api-partner-list.html', context)


@superuser_required(login_url='login')
def toggle_api_partner(request, id):
    partner = ApiPartner.objects.get(id=id)
    partner.is_active = not partner.is_active
    partner.save(update_fields=['is_active'])
    return redirect('api-partner-list')


@superuser_required(login_url='login')
def delete_api_partner(request, id):
    partner = ApiPartner.objects.get(id=id)
    partner.delete()
    return redirect('api-partner-list')
