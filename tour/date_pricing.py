"""
محاسبه‌ی «ارزون‌ترین قیمت» یک تور برای یک تاریخ برگزاری خاص (یا تاریخ پیش‌فرض تور).

قبلاً چند جای مختلف سایت (تب تاریخ‌های صفحه‌ی جزییات تور، پاپ‌آپ تاریخ‌های صفحات
شهر/کشور) هرکدوم جدا فقط قیمتِ *یک* پکیج ثابت («ارزون‌ترین پکیج بر اساس قیمت خام»)
رو به‌عنوان مرجع دنبال می‌کردن و override قیمتیِ ثبت‌شده برای بقیه‌ی پکیج‌ها رو
نمی‌دیدن. این تابع مشترک، واقعاً بین *همه‌ی* پکیج‌های قابل‌نمایش اون تاریخ (با در
نظر گرفتن override قیمت/مخفی‌بودن/پکیج مخصوص همون تاریخ) ارزون‌ترین رو پیدا می‌کنه.
"""
from tour.models import DatePlanPackagePrice, Package, Tour, date_plan


def compute_tour_min_price(packages, dp=None, overrides=None):
    """
    packages: لیست/کوئری‌ست از instance های Package مربوط به یک تور (select_related روی
        Pcry/fr_Pcry توصیه می‌شه ولی لازم نیست).
    dp: یک date_plan یا None (یعنی تاریخ پیش‌فرض تور).
    overrides: اگه از قبل دیکشنری {package_id: DatePlanPackagePrice} رو داشته باشی
        (مثلاً تو حالت دسته‌ای برای چند تور)، پاسش بده تا کوئری اضافه زده نشه.

    خروجی: دیکشنری {price, price_dollar, currency, currency_foreign} برای ارزون‌ترین
    گزینه‌ی قابل‌نمایش، یا None اگه هیچ پکیج قابل‌نمایشی نبود.
    """
    packages = list(packages)
    if overrides is None:
        overrides = {}
        if dp:
            overrides = {
                o.package_id: o
                for o in DatePlanPackagePrice.objects.filter(
                    date_plan=dp, package_id__in=[p.id for p in packages]
                )
            }
    best = None
    for pkg in packages:
        # پکیج مخصوص یک تاریخ دیگه (نه همین تاریخ) هیچ‌وقت تو این تاریخ نمایش داده نمی‌شه
        if pkg.exclusive_date_plan_id and (not dp or pkg.exclusive_date_plan_id != dp.id):
            continue
        override = overrides.get(pkg.id)
        if override:
            if override.is_hidden:
                continue
            price = override.DoubleBedPrice
            price_dollar = override.DoubleBedPrice_doller
            currency = override.currency or pkg.Pcry
            currency_foreign = override.foreign_currency or pkg.fr_Pcry
        elif pkg.exclusive_date_plan_id:
            # پکیج مخصوص همین تاریخه و override نداره یعنی قیمت خودش از قبل نهایی‌ه
            price = pkg.DoubleBedPrice
            price_dollar = pkg.DoubleBedPrice_doller
            currency = pkg.Pcry
            currency_foreign = pkg.fr_Pcry
        else:
            price = int(pkg.DoubleBedPrice or 0)
            price_dollar = int(pkg.DoubleBedPrice_doller or 0)
            currency = pkg.Pcry
            currency_foreign = pkg.fr_Pcry
            if dp:
                adj = int(dp.price or 0)
                adj_foreign = int(dp.price_dollar or 0)
                dollar_type = dp.price_dollar_type if dp.price_dollar_type in ('افزایش', 'کاهش') else dp.price_type
                if adj and dp.price_type in ('افزایش', 'کاهش'):
                    sign = 1 if dp.price_type == 'افزایش' else -1
                    price = price + sign * adj
                if adj_foreign and dollar_type in ('افزایش', 'کاهش'):
                    sign_f = 1 if dollar_type == 'افزایش' else -1
                    price_dollar = price_dollar + sign_f * adj_foreign
        if price is None:
            continue
        if best is None or price < best['price']:
            best = {
                'price': price,
                'price_dollar': price_dollar or 0,
                'currency': str(currency) if currency else 'تومان',
                'currency_foreign': str(currency_foreign) if currency_foreign else 'دلار',
            }
    return best


def tour_card_packages(tour):
    """
    لیست پکیج‌های یک تور برای «کارت لیست تور»، وقتی که قیمت اولین پکیج (که قالب
    به‌عنوان «شروع قیمت از» نشون می‌ده) با ارزون‌ترین قیمت مؤثرِ تاریخ پیش‌فرض همون
    تور جایگزین شده باشه.

    پکیج‌های مخصوص یک تاریخ خاص از لیست نمایشی کنار گذاشته می‌شن، ولی تو محاسبه‌ی
    ارزون‌ترین قیمتِ تاریخ پیش‌فرض (اگه مخصوص همون تاریخ باشن) لحاظ می‌شن.
    """
    if not tour:
        return []
    every = list(Package.objects.filter(TourName_id=tour.id).select_related('Pcry', 'fr_Pcry'))
    display = [p for p in every if not p.exclusive_date_plan_id]
    display.sort(key=lambda p: ((p.DoubleBedPrice or 0), (p.DoubleBedPrice_doller or 0)))
    if not display:
        return []
    base_dp = date_plan.objects.filter(tour_id=tour.id, start_date=tour.StartDate).first()
    best = compute_tour_min_price(every, base_dp)
    if best:
        display[0].DoubleBedPrice = best['price']
        display[0].DoubleBedPrice_doller = best['price_dollar']
        display[0].DollerPrice = None
    return display


def tour_card_packages_bulk(tours):
    """
    نسخه‌ی دسته‌ای tour_card_packages برای صفحات لیست تور.

    به‌جای چند کوئری به‌ازای هر کارت (که رو صفحات لیست به صدها کوئری می‌رسید)،
    کل کار با ۳ کوئری انجام می‌شه. خروجی: دیکشنری {tour_id: [packages...]}
    """
    tours = [t for t in tours if t]
    if not tours:
        return {}
    tour_ids = [t.id for t in tours]

    # ۱) همه‌ی پکیج‌های این تورها
    by_tour = {}
    for p in Package.objects.filter(TourName_id__in=tour_ids).select_related('Pcry', 'fr_Pcry'):
        by_tour.setdefault(p.TourName_id, []).append(p)

    # ۲) تاریخ برگزاریِ منطبق با تاریخ شروع هر تور (اگه وجود داشته باشه)
    start_by_tour = {t.id: t.StartDate for t in tours}
    base_dp_by_tour = {}
    for dp in date_plan.objects.filter(tour_id__in=tour_ids):
        if start_by_tour.get(dp.tour_id) and dp.start_date == start_by_tour[dp.tour_id]:
            base_dp_by_tour.setdefault(dp.tour_id, dp)

    # ۳) قیمت‌های دستیِ ثبت‌شده برای همون تاریخ‌ها
    overrides_by_dp = {}
    dp_ids = [dp.id for dp in base_dp_by_tour.values()]
    if dp_ids:
        for o in DatePlanPackagePrice.objects.filter(date_plan_id__in=dp_ids):
            overrides_by_dp.setdefault(o.date_plan_id, {})[o.package_id] = o

    result = {}
    for tour in tours:
        every = by_tour.get(tour.id, [])
        display = [p for p in every if not p.exclusive_date_plan_id]
        display.sort(key=lambda p: ((p.DoubleBedPrice or 0), (p.DoubleBedPrice_doller or 0)))
        if not display:
            result[tour.id] = []
            continue
        base_dp = base_dp_by_tour.get(tour.id)
        ov = overrides_by_dp.get(base_dp.id, {}) if base_dp else {}
        best = compute_tour_min_price(every, base_dp, overrides=ov)
        if best:
            display[0].DoubleBedPrice = best['price']
            display[0].DoubleBedPrice_doller = best['price_dollar']
            display[0].DollerPrice = None
        result[tour.id] = display
    return result


def apply_own_base_price_bulk(packages):
    """
    برای لیستی از پکیج‌ها (مثلاً «تورهایی که این هتل داخلشونه»): قیمت نمایشی هر
    پکیج با قیمت دستیِ *خودِ همون پکیج* برای تاریخ پیش‌فرض تورش جایگزین می‌شه.
    برخلاف tour_card_packages_bulk اینجا ارزون‌ترین پکیجِ تور ملاک نیست، چون هر
    ردیف مربوط به یک پکیج مشخصه.
    """
    packages = [p for p in packages if p]
    if not packages:
        return packages
    tour_ids = {p.TourName_id for p in packages}
    starts = dict(Tour.objects.filter(id__in=tour_ids).values_list('id', 'StartDate'))
    base_dp_by_tour = {}
    for dp in date_plan.objects.filter(tour_id__in=tour_ids):
        if starts.get(dp.tour_id) and dp.start_date == starts[dp.tour_id]:
            base_dp_by_tour.setdefault(dp.tour_id, dp)
    if not base_dp_by_tour:
        return packages
    wanted = {(base_dp_by_tour[p.TourName_id].id, p.id)
              for p in packages if p.TourName_id in base_dp_by_tour}
    overrides = {}
    if wanted:
        for o in DatePlanPackagePrice.objects.filter(
            date_plan_id__in={d for d, _ in wanted}, package_id__in={p for _, p in wanted}
        ):
            overrides[(o.date_plan_id, o.package_id)] = o
    for pkg in packages:
        dp = base_dp_by_tour.get(pkg.TourName_id)
        if not dp:
            continue
        o = overrides.get((dp.id, pkg.id))
        if o and not o.is_hidden:
            pkg.DoubleBedPrice = o.DoubleBedPrice
            pkg.DoubleBedPrice_doller = o.DoubleBedPrice_doller
    return packages


_HOTEL_OVERRIDE_PAIRS = [
    ('HotelName', 'hotel_override'),
    ('Mhotel', 'mhotel_override'),
    ('M1hotel', 'm1hotel_override'),
    ('M2hotel', 'm2hotel_override'),
    ('M3hotel', 'm3hotel_override'),
]

_VIEW_SERVICE_PAIRS = [
    ('view_hotel', 'service_hotel'),
    ('view_mhotel', 'service_mhotel'),
    ('view_m1hotel', 'service_m1hotel'),
    ('view_m2hotel', 'service_m2hotel'),
    ('view_m3hotel', 'service_m3hotel'),
]

_SOLD_OUT_FIELDS = [
    'hotel_sold_out', 'mhotel_sold_out', 'm1hotel_sold_out',
    'm2hotel_sold_out', 'm3hotel_sold_out',
]

_PRICE_FIELDS = [
    'DoubleBedPrice', 'SingleBedPrice', 'BabyWithBedPrice', 'BabyWithoutBedPrice', 'InfontPrice',
    'DoubleBedPrice_doller', 'SingleBedPrice_doller', 'BabyWithBedPrice_doller',
    'BabyWithoutBedPrice_doller', 'InfontPrice_doller',
]


def packages_for_date(tour, dp=None):
    """
    پکیج‌های قابل‌نمایش یک تور برای یک تاریخ برگزاری، وقتی که قیمت/هتل/ویو/سرویس
    مؤثرِ همون تاریخ روشون اعمال شده باشه. پکیج‌های «حذف‌شده برای این تاریخ» و
    پکیج‌های مخصوصِ تاریخ‌های دیگه از لیست کنار گذاشته می‌شن.

    اگه dp داده نشه و تور یه date_plan دقیقاً با تاریخ شروع خودش داشته باشه، همون
    به‌عنوان تاریخ جاری در نظر گرفته می‌شه (مثل صفحه‌ی جزییات تور).
    """
    if not tour:
        return []
    if dp is None:
        dp = date_plan.objects.filter(tour_id=tour.id, start_date=tour.StartDate).first()

    qs = Package.objects.filter(TourName_id=tour.id).select_related(
        'Pcry', 'fr_Pcry', 'HotelName', 'Mhotel', 'M1hotel', 'M2hotel', 'M3hotel',
        'M4hotel', 'exclusive_date_plan'
    ).order_by('DoubleBedPrice', 'DoubleBedPrice_doller')
    packages = [
        p for p in qs
        if not p.exclusive_date_plan_id or (dp and p.exclusive_date_plan_id == dp.id)
    ]
    if not dp or not packages:
        return packages

    overrides = {
        o.package_id: o
        for o in DatePlanPackagePrice.objects.filter(
            date_plan=dp, package_id__in=[p.id for p in packages]
        ).select_related(
            'hotel_override', 'mhotel_override', 'm1hotel_override',
            'm2hotel_override', 'm3hotel_override',
        )
    }
    adj = int(dp.price or 0)
    adj_foreign = int(dp.price_dollar or 0)
    adj_infant = int(dp.infant_price or 0)
    adj_infant_foreign = int(dp.infant_price_dollar or 0)
    dollar_type = dp.price_dollar_type if dp.price_dollar_type in ('افزایش', 'کاهش') else dp.price_type
    sign = 1 if dp.price_type == 'افزایش' else -1 if dp.price_type == 'کاهش' else 0
    sign_f = 1 if dollar_type == 'افزایش' else -1 if dollar_type == 'کاهش' else 0

    result = []
    for pkg in packages:
        override = overrides.get(pkg.id)
        if override:
            if override.is_hidden:
                continue
            for hotel_attr, override_field in _HOTEL_OVERRIDE_PAIRS:
                swapped = getattr(override, override_field)
                if swapped:
                    setattr(pkg, hotel_attr, swapped)
            for view_field, service_field in _VIEW_SERVICE_PAIRS:
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
            for field in _PRICE_FIELDS:
                setattr(pkg, field, getattr(override, field))
            # «تکمیل ظرفیت» هر هتل هم مثل قیمت، مقدارِ همین تاریخ است. صفحهٔ
            # تنظیم قیمت هر تاریخ هر پنج چک‌باکس را در هر ذخیره می‌نویسد، پس
            # ردیف override مقدار معتبر این تاریخ را دارد.
            for field in _SOLD_OUT_FIELDS:
                setattr(pkg, field, getattr(override, field))
        elif not pkg.exclusive_date_plan_id:
            # پکیج مخصوص همین تاریخ، قیمتش از قبل نهایی‌ه و اختلاف عمومی روش اعمال نمی‌شه
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
        result.append(pkg)
    return result
