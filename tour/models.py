
import secrets

from django.core.validators import FileExtensionValidator
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from multiselectfield import MultiSelectField
from django_resized import ResizedImageField
from hotels.models import Hotel_Data

MENU_POSITION = [
    ('1', 'ستون اول'),
    ('2', 'ستون دوم'),
    ('3', 'ستون سوم'),
    ('4', 'ستون چهارم'),
]

ORDER_STATUS = [
    ('ثبت شده', 'ثبت شده'), ('ارسال مدارک', 'ارسال مدارک'),
    ('در انتظار تایید', 'در انتظار تایید'), ('تایید شده', 'تایید شده')
    ]

FLIGHT_CLASS = [
    ('', 'انتخاب کلاس پرواز'), ('ECONOMY', 'ECONOMY'), ('BUSSINESS', 'BUSSINESS')
]

RATING = [
    ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')
]
SERVICE = [
    ('OR','OR'),('BB','BB'),('HB','HB'),('FB','FB'),('ALL','ALL'),('U ALL','U ALL'),('max ALL','max ALL')
]
CITY_TRANSFER = [
    ('', 'بدون ترانسفر'),
    ('bus', 'اتوبوس'),
    ('train', 'قطار'),
    ('flight', 'پرواز داخلی'),
    ('boat', 'قایق'),
]
HOTEL_SERVICES = [
    ('پارکینگ', 'پارکینگ'), ('آسانسور', 'آسانسور'), ('شاتل', 'شاتل')
    , ('ترانسفر فرودگاهی', 'ترانسفر فرودگاهی'),
     ('فروشگاه در محل', 'فروشگاه در محل'),
    ('فروشگاه در هتل', 'فروشگاه در هتل'),
    ('نزدیک به فرودگاه', 'نزدیک به فرودگاه'), ('نزدیک به ساحل', 'نزدیک به ساحل'),
    ('فضای سبز', 'فضای سبز'), ('ساحل اختصاصی', 'ساحل اختصاصی'), ('اینترنت رایگان در لابی', 'اینترنت رایگان در لابی'),
    ('سالن کنفرانس', 'سالن کنفرانس'), ('سالن همایش', 'سالن همایش'), ('اجاره ماشین', 'اجاره ماشین'),
    ('انبار چمدان', 'انبار چمدان'),
    ('رستوران', 'رستوران'), ('کافی شاپ', 'کافی شاپ'), ('صرافی', 'صرافی'),
    ('محل مخصوص سیگار کشیدن', 'محل مخصوص سیگار کشیدن'),
    ('اتاق خانوادگی', 'اتاق خانوادگی'), ('محل سیگار ممنوع', 'محل سیگار ممنوع'),
    ('امکانات برای معلولین', 'امکانات برای معلولین'),
    ('لپ تاپ', 'لپ تاپ'), ('ورود حیوانات مجاز', 'ورود حیوانات مجاز')
]

ROOM_SERVICES = [
    ('اینترنت رایگان در اتاق', 'اینترنت رایگان در اتاق'), ('تراس/بالکن', 'تراس/بالکن'), ('چای/قهوه ساز', 'چای/قهوه ساز'),
    ('وان', 'وان'),
    ('صندوق امانات', 'صندوق امانات'), ('کمد و جالباسی', 'کمد و جالباسی'), ('تهویه مطبوع', 'تهویه مطبوع'),
    ('حوله و دمپایی', 'حوله و دمپایی'),
    ('سشوار', 'سشوار'), ('اتو', 'اتو'), ('سنسور دودیاب/ضد حریق', 'سنسور دودیاب/ضد حریق'),
    ('آلارم بیدار باش', 'آلارم بیدار باش'),
    ('سیستم گرمایش', 'سیستم گرمایش'), ('تلوزیون/ماهواره', 'تلویزیون/ماهواره'),
    ('عایق صدا', 'عایق صدا'), ('میز مطالعه', 'میز مطالعه'),
    ('نور گیر', 'نور گیر'), ('دزدگیر', 'دزدگیر'), ('منظره شهری', 'منظره شهری'), ('آشپزخانه','آشپزخانه'), ('لوازم بهداشتي','لوازم بهداشتي')
]

SERVICES = [
    (' سرویس اتاق 24 ساعته', 'سرویس اتاق 24 ساعته'), ('صبحانه در اتاق', 'صبحانه در اتاق'),
    ('خدمات پزشکی', 'خدمات پزشکی'), ('خشکشویی', 'خشکشویی'), ('نظافت روزانه', 'نظافت روزانه'), ('پذیرش 24 ساعته', 'پذیرش 24 ساعته'),
    ('غذای کودک', 'غذای کودک'), ('غذای رژیمی', 'غذای رژیمی'),('صبحانه', 'صبحانه'),('خدمات زیبایی', 'خدمات زیبایی'),

    ]

INTERTAINMENT = [
    ('استخر روباز', 'استخر روباز'), ('استخر سرپوشیده', 'استخر سرپوشیده'), ('سونا/جکوزی', 'سونا/جکوزی'),
    ('پارک آبی', 'پارک آبی'), ('حمام ترکی', 'حمام ترکی'), ('ماساژ', 'ماساژ'), ('مینی بار', 'مینی بار'),
    ('مرکز اسپا و سلامتی', 'مرکز اسپا و سلامتی'), ('استخر کودک', 'استخر کودک'),
    ('سالن بازی کودکان', 'سالن بازی کودکان'),
    ('پارک کودک', 'پارک کودک'), (' تفريحات آبي', ' تفريحات آبي'), (' قايقراني', ' قايقراني'),
    ('غواصی', 'غواصی'), ('سالن بدنسازی', 'سالن بدنسازی'), ('بیلیارد', 'بیلیارد'),
    ('دارت', 'دارت'), ('تنیس', 'تنیس'), ('کلاس یوگا', 'کلاس یوگا'), ('سولاريوم', 'سولاريوم'), ('ماهيگيري', 'ماهيگيري'),
    ('اسنک بار', 'اسنک بار'), ('اتاق گیم', 'اتاق گیم'), ('بار', 'بار'), ('پینگ پونگ', 'پینگ پونگ'),
    ('بولینگ', 'بولینگ'), (' اسکی', ' اسکی'),('اجراي برنامه هاي شاد', 'اجراي برنامه هاي شاد'),('موسیقی زنده', 'موسیقی زنده'),('دی جی', 'دی جی'),
    ('دوچرخه سواری', 'دوچرخه سواری'), ('گلف', 'گلف'), ('کارائوکه', 'کارائوکه'), ('صندلی ساحلی', 'صندلی ساحلی'),('کلوپ شبانه','کلوپ شبانه')
    ]

MEDIATYPE = [
    ("video", "Video"),
    ("audio", "Audio"),
    ("image", "Image"),
    ("document", "Document"),
]

ROBOTS_CHOICES = [
    ('INDEX,FOLLOW', 'Index, Follow - (پیش‌فرض) نمایش در نتایج و دنبال کردن لینک‌ها'),
    ('INDEX,NOFOLLOW', 'Index, No Follow - نمایش در نتایج، دنبال نکردن لینک‌ها'),
    ('NOINDEX,FOLLOW', 'No Index, Follow - عدم نمایش در نتایج، دنبال کردن لینک‌ها'),
    ('NOINDEX,NOFOLLOW', 'No Index, No Follow - عدم نمایش در نتایج و دنبال نکردن لینک‌ها'),
]

class viewCounter(models.Model):
    indexView = models.IntegerField(default=0)
    toursView = models.IntegerField(default=0)
    hotelsView = models.IntegerField(default=0)
    blogView = models.IntegerField(default=0)
    contacView = models.IntegerField(default=0)
    aboutView = models.IntegerField(default=0)
    
class TourMenu(models.Model):
    MenuTitle = models.CharField(max_length=150)
    MenuDesc = RichTextUploadingField(max_length=3000, null=True, blank=True)
    slug = models.SlugField(blank=True, null=True)
    show_meu = models.BooleanField(default=False)
    meta_keywords = models.CharField(max_length=150, null=True, blank=True)
    meta_description = models.TextField(max_length=300, null=True, blank=True)
    page_title = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.MenuTitle

    class Meta:
        verbose_name = 'اطلاعات منو تور'
        verbose_name_plural = 'اطلاعات منو تور'

class Currency(models.Model):
    Title = models.CharField(max_length=300)

    def __str__(self):
        return self.Title

class Country(models.Model):
    TitleC = models.CharField(max_length=300)
    Flagimg = models.ImageField(upload_to='country-flag', null=True, blank=True)
    tourmk = models.CharField(max_length=500, null=True, blank=True)
    Description = RichTextUploadingField(max_length=35000, null=True, blank=True)
    Description_anchor = RichTextUploadingField(max_length=25000, null=True, blank=True)
    hotel_page_Description = RichTextUploadingField(max_length=25000, null=True, blank=True)
    hotel_page_Description_anchor = RichTextUploadingField(max_length=25000, null=True, blank=True)
    tourmd = models.CharField(max_length=150, null=True, blank=True)
    hotelmk = models.CharField(max_length=500, null=True, blank=True)
    hotelmd = models.CharField(max_length=150, null=True, blank=True)
    tltitle = models.CharField(max_length=150, null=True, blank=True)
    hltitle = models.CharField(max_length=150, null=True, blank=True)
    showInMenu = models.BooleanField(default=True)
    hotel_page = models.BooleanField(default=True)
    country_iamge = ResizedImageField(force_format='WEBP', quality=75, upload_to='media/country-image', null=True, blank=True)
    country_icon = ResizedImageField(force_format='WEBP', quality=75, upload_to='media/country-image/icon', null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, null=False)
    menu_position = models.CharField(max_length=2, choices=MENU_POSITION, default='1')
    menu_order = models.IntegerField(default=1)
    tour_meta_robots = models.CharField(
        max_length=50,
        choices=ROBOTS_CHOICES,
        default='INDEX,FOLLOW',
        verbose_name='وضعیت نمایش در موتورهای جستجو (SEO)',
        help_text='تنظیم کنید که این صفحه در گوگل دیده شود یا خیر'
    )
    hotel_meta_robots = models.CharField(
        max_length=50,
        choices=ROBOTS_CHOICES,
        default='INDEX,FOLLOW',
        verbose_name='وضعیت نمایش در موتورهای جستجو (SEO)',
        help_text='تنظیم کنید که این صفحه در گوگل دیده شود یا خیر'
    )


    class Meta:
        ordering = ['-id']
    def __str__(self):
        return self.TitleC

class City(models.Model):
    CountryName = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    Name = models.CharField(max_length=300)
    cityImg = models.ImageField(upload_to='city', null=True, blank=True)
    cityIcon = models.ImageField(upload_to='city/icon', null=True, blank=True)
    Description = RichTextUploadingField(max_length=25000, null=True, blank=True)
    Description_anchor = RichTextUploadingField(max_length=25000, null=True, blank=True)
    hotel_page_Description = RichTextUploadingField(max_length=25000, null=True, blank=True)
    hotel_page_Description_anchor= RichTextUploadingField(max_length=25000, null=True, blank=True)
    showInMenu = models.BooleanField(default=True)
    hotel_page = models.BooleanField(default=True)
    slug = models.SlugField(max_length=255, unique=True, null=False)
    tourmk = models.CharField(max_length=500, null=True, blank=True)
    tourmd = models.CharField(max_length=150, null=True, blank=True)
    hotelmk = models.CharField(max_length=500, null=True, blank=True)
    hotelmd = models.CharField(max_length=150, null=True, blank=True)
    tltitle = models.CharField(max_length=150, null=True, blank=True)
    hltitle = models.CharField(max_length=150, null=True, blank=True)
    tour_meta_robots = models.CharField(
        max_length=50,
        choices=ROBOTS_CHOICES,
        default='INDEX,FOLLOW',
        verbose_name='وضعیت نمایش در موتورهای جستجو (SEO)',
        help_text='تنظیم کنید که این صفحه در گوگل دیده شود یا خیر'
    )
    hotel_meta_robots = models.CharField(
        max_length=50,
        choices=ROBOTS_CHOICES,
        default='INDEX,FOLLOW',
        verbose_name='وضعیت نمایش در موتورهای جستجو (SEO)',
        help_text='تنظیم کنید که این صفحه در گوگل دیده شود یا خیر'
    )

    
    def __str__(self):
        return self.Name

class AirLineData(models.Model):
    Creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر ایجاد کننده')
    AirLineTitle = models.CharField(max_length=300, verbose_name='نام ایرلاین')
    AirlineLogo = ResizedImageField(force_format='WEBP', quality=100, upload_to='Air-Line-Logos', verbose_name='لوگوی ایرلاین')
    AirlineCargo = models.CharField(max_length=20, null=True, blank=True)
    Slug = models.SlugField(max_length=255, unique=True, null=False, verbose_name='لینک سئو')

    def __str__(self):
        return self.AirLineTitle

    def save(self, *args, **kwargs):
        if not self.Slug:
            self.Slug = slugify(self.AirLineTitle, allow_unicode=True)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'اطلاعات ایرلاین'
        verbose_name_plural = 'اطلاعات ایرلاین'

class Airport(models.Model):
    AirportEn = models.CharField(max_length=500)
    AirportFa = models.CharField(max_length=500)

    def __str__(self):
        return self.AirportFa + ' - ' + self.AirportEn

class Tour(models.Model):
    Creator = models.ForeignKey(User, on_delete=models.CASCADE)
    Title = models.CharField(max_length=500)
    TourMenu = models.ForeignKey(TourMenu, on_delete=models.CASCADE, null=True, blank=True)
    Tcountry = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True, related_name='tocountry')
    Tcity = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True, related_name='tour_city')
    Slug = models.SlugField(null=True, blank=True, unique=True, max_length=255)
    StartDate = models.DateField()
    EndDate = models.DateField()
    NightCount = models.CharField(max_length=10)
    Offer = models.CharField(max_length=300, null=True, blank=True)
    DayCount = models.CharField(max_length=10)
    ShortDsc = RichTextUploadingField(max_length=6000, null=True, blank=True)
    documents = RichTextUploadingField(max_length=6000, null=True, blank=True)
    Description = RichTextUploadingField(max_length=10000, null=True, blank=True)
    cancel_policy = RichTextUploadingField(null=True, blank=True, verbose_name='قوانین کنسلی')
    about_tour = RichTextUploadingField(null=True, blank=True, verbose_name='درباره تور')
    Feature = models.BooleanField(default=False)
    Installment = models.BooleanField(default=False)
    Cash = models.BooleanField(default=False)
    TourImage = ResizedImageField(force_format='WEBP', quality=75,upload_to='tour-images', null=True, blank=True)
    MetaDescription = models.TextField(max_length=350, null=True, blank=True)
    MetaKeywords = models.TextField(max_length=200, null=True, blank=True)
    PubTour = models.BooleanField(default=True)
    OfferShow = models.BooleanField(default=False)
    TourPdf = models.FileField(upload_to='uploads/%Y/%m/%d/', null=True, blank=True)
    viewCount = models.IntegerField(default=0, null=True, blank=True)
    tstitle = models.CharField(max_length=1000, null=True, blank=True)
    updateDate = models.DateTimeField(auto_now=True)
    pdfAvb = models.BooleanField(default=False)
    pdfdesc = models.TextField(max_length=2000, null=True, blank=True)
    add_peice_single = models.IntegerField(default=0, null=True, blank=True)
    add_peice_dubel = models.IntegerField(default=0, null=True, blank=True)
    add_peice_with_bed = models.IntegerField(default=0, null=True, blank=True)
    add_peice_without_bed = models.IntegerField(default=0, null=True, blank=True)
    add_peice_infont = models.IntegerField(default=0, null=True, blank=True)
    satrap_gte = models.BooleanField(default=False)
    norooz = models.BooleanField(default=False)
    tour_main = models.ImageField(upload_to='media/tour_img', null=True, blank=True)
    origin_city = models.ForeignKey(City, null=True, blank=True, related_name='origin_city', on_delete=models.CASCADE)
    spacial_lable = models.CharField(max_length=50, null=True, blank=True)
    meta_robots = models.CharField(
        max_length=50,
        choices=ROBOTS_CHOICES,
        default='INDEX,FOLLOW',
        verbose_name='وضعیت نمایش در موتورهای جستجو (SEO)',
        help_text='تنظیم کنید که این صفحه در گوگل دیده شود یا خیر'
    )
    custom_categories = models.ManyToManyField(
        'CustomTourCategory',
        blank=True,
        related_name='tours',
        verbose_name='دسته‌بندی‌های سفارشی'
    )
    force_pub = models.BooleanField(default=False, verbose_name='نمایش تور تاریخ گذشته')


    def __str__(self):
        return self.Title

    def get_absolute_url(self):
        kwargs = {
            'id':self.id,
            'Slug': self.Slug
        }
        return reverse('tour-detail', kwargs=kwargs)

    class Meta:
        ordering = ('Tcity',)
        verbose_name = 'اطلاعات تورها'
        verbose_name_plural = 'اطلاعات تورها'

class TourCity(models.Model):
    CyName = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    CtName = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    Airline = models.ForeignKey(AirLineData, on_delete=models.CASCADE, null=True, blank=True)
    FromAirport = models.ForeignKey(Airport, on_delete=models.CASCADE, null=True, blank=True, related_name='airportone')
    ToAirport = models.ForeignKey(Airport, on_delete=models.CASCADE, null=True, blank=True, related_name='airportwo')
    FlightTime = models.CharField(max_length=300, null=True, blank=True)
    FlightDuration = models.CharField(max_length=300, null=True, blank=True)
    FlightClass = models.CharField(choices=FLIGHT_CLASS, max_length=50, null=True, blank=True)
    NightCount = models.CharField(max_length=300, null=True, blank=True, default='0')
    Waiting = models.CharField(max_length=300, null=True, blank=True)
    TourName = models.ForeignKey(Tour, on_delete=models.CASCADE, null=True, blank=True)
    GTransfer = models.BooleanField(default=False)
    QTransfer = models.BooleanField(default=False)
    STransfer = models.BooleanField(default=False)
    flight_return = models.BooleanField(default=False)
    flight_inbound = models.BooleanField(default=False)
    GDest = models.CharField(max_length=300, null=True, blank=True)
    
##    def __str__(self):
##        return self.Airline.AirLineTitle

class CustomTourCategory(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)
    description = RichTextUploadingField(max_length=35000, null=True, blank=True)

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='children',
    )
    countries = models.ManyToManyField(
        Country,
        blank=True,
        related_name='tour_categories',
    )
    cities = models.ManyToManyField(
        City,
        blank=True,
        related_name='tour_categories',
    )
    image = models.ImageField(upload_to='tour/category-images/%Y/%m/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    meta_title = models.CharField(max_length=150, null=True, blank=True)
    meta_keyword = models.CharField(max_length=150, null=True, blank=True)
    meta_description = models.CharField(max_length=150, null=True, blank=True)
    meta_robots = models.CharField(
            max_length=50,
            choices=ROBOTS_CHOICES,
            default='INDEX,FOLLOW',
            verbose_name='وضعیت نمایش در موتورهای جستجو (SEO)',
            help_text='تنظیم کنید که این صفحه در گوگل دیده شود یا خیر'
    )
    
    def sync_locations(self):
        tours = self.tours.select_related('Tcity', 'Tcountry')
        cities = set()
        countries = set()

        for tour in tours:
            if tour.Tcity_id:
                cities.add(tour.Tcity_id)

            if tour.Tcountry_id:
                countries.add(tour.Tcountry_id)

        self.cities.set(cities)
        self.countries.set(countries)

        
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} → {self.name}"
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

class TourCategoryFAQ(models.Model):
    category = models.ForeignKey(CustomTourCategory, on_delete=models.CASCADE, null=True, blank=True)
    question = models.CharField(max_length=500, null=True, blank=True)
    answer = RichTextUploadingField(max_length=5000, null=True, blank=True, config_name='col_lg_6')

class CityCountryMedia(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="city_media", null=True, blank=True )
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="country_media", null=True, blank=True )
    title = models.CharField( max_length=255, blank=True )
    media_type = models.CharField( max_length=20, choices=MEDIATYPE )
    file = models.FileField( upload_to="media/tour_media/%Y/%m/" )
    thumbnail = models.ImageField( upload_to="media/tour_media/thumbs/%Y/%m/", blank=True, null=True )
    duration_seconds = models.PositiveIntegerField( blank=True, null=True )
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["sort_order", "-created_at"]

    def __str__(self):
        return f"{self.tour.title} - {self.media_type}"

class MainPackage(models.Model):
    Creator = models.ForeignKey(User, on_delete=models.CASCADE)
    PackageName = models.CharField(max_length=300)


    def __str__(self):
        return self.PackageName

    class Meta:
        verbose_name = 'Main Package'
        verbose_name_plural = 'Main Package'

class Package(models.Model):
    is_sold_out = models.BooleanField(default=False, verbose_name='پر شده / موجود نیست')
    VIEW = [
        ('','انتخاب ویو'),
        ('land View','Land View'),
        ('Sea View','Sea View'),
        ('Seaside View','Seaside View'),
    ]
    Creator = models.ForeignKey(User, on_delete=models.CASCADE)
    MainPkg = models.ForeignKey(MainPackage, on_delete=models.CASCADE)
    TourName = models.ForeignKey(Tour, on_delete=models.CASCADE)
    HotelName = models.ForeignKey(Hotel_Data, on_delete=models.CASCADE)
    view_hotel = models.CharField(choices=VIEW, max_length=300, null=True, blank=True)
    service_hotel = models.CharField(choices=SERVICE, max_length=300, null=True, blank=True)
    Mhotel = models.ForeignKey(Hotel_Data, on_delete=models.CASCADE, null=True, blank=True, related_name='mhotel')
    view_mhotel = models.CharField(choices=VIEW, max_length=300, null=True, blank=True)
    service_mhotel = models.CharField(choices=SERVICE, max_length=300, null=True, blank=True)
    M1hotel = models.ForeignKey(Hotel_Data, on_delete=models.CASCADE, null=True, blank=True, related_name='m1hotel')
    view_m1hotel = models.CharField(choices=VIEW, max_length=300, null=True, blank=True)
    service_m1hotel = models.CharField(choices=SERVICE, max_length=300, null=True, blank=True)
    M2hotel = models.ForeignKey(Hotel_Data, on_delete=models.CASCADE, null=True, blank=True, related_name='m2hotel')
    view_m2hotel = models.CharField(choices=VIEW, max_length=300, null=True, blank=True)
    service_m2hotel = models.CharField(choices=SERVICE, max_length=300, null=True, blank=True)
    M3hotel = models.ForeignKey(Hotel_Data, on_delete=models.CASCADE, null=True, blank=True, related_name='m3hotel')
    view_m3hotel = models.CharField(choices=VIEW, max_length=300, null=True, blank=True)
    service_m3hotel = models.CharField(choices=SERVICE, max_length=300, null=True, blank=True)
    M4hotel = models.ForeignKey(Hotel_Data, on_delete=models.CASCADE, null=True, blank=True, related_name='m4hotel')
    view_m4hotel = models.CharField(choices=VIEW, max_length=300, null=True, blank=True)
    service_m4hotel = models.CharField(choices=SERVICE, max_length=300, null=True, blank=True)
    hotel_sold_out = models.BooleanField(default=False, verbose_name='تکمیل ظرفیت - هتل اول')
    mhotel_sold_out = models.BooleanField(default=False, verbose_name='تکمیل ظرفیت - هتل دوم')
    m1hotel_sold_out = models.BooleanField(default=False, verbose_name='تکمیل ظرفیت - هتل سوم')
    m2hotel_sold_out = models.BooleanField(default=False, verbose_name='تکمیل ظرفیت - هتل چهارم')
    m3hotel_sold_out = models.BooleanField(default=False, verbose_name='تکمیل ظرفیت - هتل پنجم')
    transfer_mhotel = models.CharField(choices=CITY_TRANSFER, max_length=20, null=True, blank=True, verbose_name='ترانسفر تا هتل دوم')
    transfer_m1hotel = models.CharField(choices=CITY_TRANSFER, max_length=20, null=True, blank=True, verbose_name='ترانسفر تا هتل سوم')
    transfer_m2hotel = models.CharField(choices=CITY_TRANSFER, max_length=20, null=True, blank=True, verbose_name='ترانسفر تا هتل چهارم')
    transfer_m3hotel = models.CharField(choices=CITY_TRANSFER, max_length=20, null=True, blank=True, verbose_name='ترانسفر تا هتل پنجم')
    DoubleBedPrice = models.IntegerField(default=0)
    SingleBedPrice = models.IntegerField(default=0)
    BabyWithBedPrice = models.IntegerField(default=0)
    BabyWithoutBedPrice = models.IntegerField(default=0)
    InfontPrice = models.IntegerField(default=0)
    DoubleBedPrice_doller = models.IntegerField(default=0, null=True, blank=True)
    SingleBedPrice_doller = models.IntegerField(default=0, null=True, blank=True)
    BabyWithBedPrice_doller = models.IntegerField(default=0, null=True, blank=True)
    BabyWithoutBedPrice_doller = models.IntegerField(default=0, null=True, blank=True)
    InfontPrice_doller = models.IntegerField(default=0, null=True, blank=True)
    DollerPrice = models.CharField(max_length=300, null=True, blank=True)
    Pcry = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True, blank=True)
    fr_Pcry = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True, blank=True, related_name="forign_prcy")
    view = models.CharField(choices=VIEW, max_length=300, null=True, blank=True)
    exclusive_date_plan = models.ForeignKey('date_plan', on_delete=models.CASCADE, null=True, blank=True,
                                             related_name='exclusive_packages',
                                             verbose_name='مخصوص این تاریخ برگزاری (خالی یعنی برای همه تاریخ‌ها)')

    @property
    def is_toman(self):
        if not self.Pcry_id:
            return False
        return 'تومان' in str(self.Pcry)

    def __str__(self):
        formated_price = "{:,.0f}".format(int(self.DoubleBedPrice))
        return f"{self.HotelName.HotelName} - {formated_price} تومان"

    class Meta:
        verbose_name = 'پکیج ها '
        verbose_name_plural = 'پکیج ها '

class date_plan(models.Model):
    TYPE = [
        ('','انتخاب نوع اختلاف قیمت'),
        ('طبق پکیج اصلی','طبق پکیج اصلی'),
        ('افزایش','افزایش'),
        ('کاهش','کاهش'),
    ]
    CURRENCY = [
        ('تومان', 'تومان'),
        ('دلار', 'دلار'),
    ]
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.IntegerField(default=0, verbose_name='اختلاف قیمت ارز اول')
    price_dollar = models.IntegerField(default=0, null=True, blank=True, verbose_name='اختلاف قیمت ارز دوم')
    price_currency = models.CharField(choices=CURRENCY, max_length=10, default='تومان')
    price_type = models.CharField(choices=TYPE, max_length=300)
    price_dollar_type = models.CharField(choices=TYPE, max_length=300, default='طبق پکیج اصلی', null=True, blank=True, verbose_name='نوع اختلاف ارز دوم')
    infant_price = models.IntegerField(default=0, null=True, blank=True, verbose_name='افزایش قیمت نوزاد ارز اول')
    infant_price_dollar = models.IntegerField(default=0, null=True, blank=True, verbose_name='افزایش قیمت نوزاد ارز دوم')

    def __str__(self):
        return f"{self.tour} ({self.start_date} - {self.end_date})"


class DatePlanPackagePrice(models.Model):
    date_plan = models.ForeignKey(date_plan, on_delete=models.CASCADE, related_name='package_prices')
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='date_plan_overrides')
    DoubleBedPrice = models.IntegerField(default=0, verbose_name='قیمت اتاق دوتخته')
    SingleBedPrice = models.IntegerField(default=0, verbose_name='قیمت اتاق یک تخته')
    BabyWithBedPrice = models.IntegerField(default=0, verbose_name='قیمت کودک با تخت')
    BabyWithoutBedPrice = models.IntegerField(default=0, verbose_name='قیمت کودک بدون تخت')
    InfontPrice = models.IntegerField(default=0, verbose_name='قیمت نوزاد')
    DoubleBedPrice_doller = models.IntegerField(default=0, verbose_name='قیمت اتاق دوتخته (ارز دوم)')
    SingleBedPrice_doller = models.IntegerField(default=0, verbose_name='قیمت اتاق یک تخته (ارز دوم)')
    BabyWithBedPrice_doller = models.IntegerField(default=0, verbose_name='قیمت کودک با تخت (ارز دوم)')
    BabyWithoutBedPrice_doller = models.IntegerField(default=0, verbose_name='قیمت کودک بدون تخت (ارز دوم)')
    InfontPrice_doller = models.IntegerField(default=0, verbose_name='قیمت نوزاد (ارز دوم)')
    hotel_sold_out = models.BooleanField(default=False, verbose_name='تکمیل ظرفیت - هتل اول')
    mhotel_sold_out = models.BooleanField(default=False, verbose_name='تکمیل ظرفیت - هتل دوم')
    m1hotel_sold_out = models.BooleanField(default=False, verbose_name='تکمیل ظرفیت - هتل سوم')
    m2hotel_sold_out = models.BooleanField(default=False, verbose_name='تکمیل ظرفیت - هتل چهارم')
    m3hotel_sold_out = models.BooleanField(default=False, verbose_name='تکمیل ظرفیت - هتل پنجم')
    is_hidden = models.BooleanField(default=False, verbose_name='عدم نمایش پکیج در این تاریخ')
    hotel_override = models.ForeignKey(Hotel_Data, on_delete=models.SET_NULL, null=True, blank=True, related_name='date_override_hotel', verbose_name='جایگزینی هتل اول برای این تاریخ')
    mhotel_override = models.ForeignKey(Hotel_Data, on_delete=models.SET_NULL, null=True, blank=True, related_name='date_override_mhotel', verbose_name='جایگزینی هتل دوم برای این تاریخ')
    m1hotel_override = models.ForeignKey(Hotel_Data, on_delete=models.SET_NULL, null=True, blank=True, related_name='date_override_m1hotel', verbose_name='جایگزینی هتل سوم برای این تاریخ')
    m2hotel_override = models.ForeignKey(Hotel_Data, on_delete=models.SET_NULL, null=True, blank=True, related_name='date_override_m2hotel', verbose_name='جایگزینی هتل چهارم برای این تاریخ')
    m3hotel_override = models.ForeignKey(Hotel_Data, on_delete=models.SET_NULL, null=True, blank=True, related_name='date_override_m3hotel', verbose_name='جایگزینی هتل پنجم برای این تاریخ')
    view_hotel = models.CharField(choices=Package.VIEW, max_length=300, null=True, blank=True, verbose_name='ویو هتل اول برای این تاریخ')
    service_hotel = models.CharField(choices=SERVICE, max_length=300, null=True, blank=True, verbose_name='سرویس هتل اول برای این تاریخ')
    view_mhotel = models.CharField(choices=Package.VIEW, max_length=300, null=True, blank=True, verbose_name='ویو هتل دوم برای این تاریخ')
    service_mhotel = models.CharField(choices=SERVICE, max_length=300, null=True, blank=True, verbose_name='سرویس هتل دوم برای این تاریخ')
    view_m1hotel = models.CharField(choices=Package.VIEW, max_length=300, null=True, blank=True, verbose_name='ویو هتل سوم برای این تاریخ')
    service_m1hotel = models.CharField(choices=SERVICE, max_length=300, null=True, blank=True, verbose_name='سرویس هتل سوم برای این تاریخ')
    view_m2hotel = models.CharField(choices=Package.VIEW, max_length=300, null=True, blank=True, verbose_name='ویو هتل چهارم برای این تاریخ')
    service_m2hotel = models.CharField(choices=SERVICE, max_length=300, null=True, blank=True, verbose_name='سرویس هتل چهارم برای این تاریخ')
    view_m3hotel = models.CharField(choices=Package.VIEW, max_length=300, null=True, blank=True, verbose_name='ویو هتل پنجم برای این تاریخ')
    service_m3hotel = models.CharField(choices=SERVICE, max_length=300, null=True, blank=True, verbose_name='سرویس هتل پنجم برای این تاریخ')
    main_pkg = models.ForeignKey(MainPackage, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='نوع پکیج برای این تاریخ')
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, blank=True, related_name='date_plan_price_currency', verbose_name='واحد پول برای این تاریخ')
    foreign_currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, blank=True, related_name='date_plan_price_foreign_currency', verbose_name='واحد پول خارجی برای این تاریخ')
    view = models.CharField(choices=Package.VIEW, max_length=300, null=True, blank=True, verbose_name='ویو کل پکیج برای این تاریخ')
    doller_price = models.CharField(max_length=300, null=True, blank=True, verbose_name='قیمت ثابت دلاری برای این تاریخ')

    def __str__(self):
        return f"{self.date_plan} - {self.package.HotelName}"

    class Meta:
        unique_together = ('date_plan', 'package')
        verbose_name = 'قیمت دستی هتل برای تاریخ'
        verbose_name_plural = 'قیمت های دستی هتل برای تاریخ'


class TripPlan(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, null=True, blank=True)
    plan_image = ResizedImageField(force_format='WEBP', quality=75, upload_to='media/trip-plan/main-images', null=True, blank=True)
    location = models.CharField(max_length=150, null=True, blank=True)
    views = models.CharField(max_length=150, null=True, blank=True)
    services = models.CharField(max_length=150, null=True, blank=True)
    description = RichTextUploadingField(max_length=6000, null=True, blank=True, config_name='col_lg_12_full')

class related_tour_city(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='tour')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)

class ContactUs(models.Model):
    FirstName = models.CharField(max_length=300)
    LastName = models.CharField(max_length=300)
    Mobile = models.CharField(max_length=300)
    Message = models.TextField(max_length=2000)
    CreatedAt = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.FirstName

class ContactUsText(models.Model):
    TextContact = models.TextField(max_length=3000)

class AboutUs(models.Model):
    TextAbout = RichTextUploadingField(max_length=10000)
        
class SlideShow(models.Model):
    FirstImage = models.ImageField(upload_to='media/slideshow/')
    SeconedImage = models.ImageField(upload_to='media/slideshow/')
    ThiredImage = models.ImageField(upload_to='media/slideshow/')

class MemoryCategory(models.Model):
    CatName = models.CharField(max_length=500)
    parentCat = models.ForeignKey('self', related_name='Children', on_delete=models.CASCADE, null=True, blank=True)
    slug = models.SlugField(unique=True, null=False, blank=False)
    page_title = models.CharField(max_length=500, null=True, blank=True)
    meta_desc = models.CharField(max_length=500, null=True, blank=True)
    meta_keyword = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        full_path = [self.CatName]
        k = self.parentCat
        while k is not None:
            full_path.append(k.CatName)
            k = k.parentCat
        return ' - '.join(full_path[::-1])

class PMemories(models.Model):
    Name = models.CharField(max_length=300)
    Family = models.CharField(max_length=300)
    Mobile = models.CharField(max_length=100)
    Email = models.CharField(max_length=100)
    img1 = ResizedImageField(force_format='WEBP', quality=75, upload_to='media/memories/', null=True, blank=True)
    img2 = ResizedImageField(force_format='WEBP', quality=75, upload_to='media/memories/', null=True, blank=True)
    Message = RichTextUploadingField(config_name='col_lg_8', null=True, blank=True)
    publish = models.BooleanField(default=False, null=True, blank=True)
    viewCount = models.IntegerField(default=0, null=True, blank=True)
    created_date = models.DateField(auto_now_add=True, null=True, blank=True)
    headline = models.CharField(max_length=200, null=True, blank=True)
    category = models.ForeignKey(MemoryCategory, on_delete=models.CASCADE, null=True, blank=True)
    slug = models.SlugField(blank=True)
    metaKeyword = models.TextField(max_length=300, null=True, blank=True)
    metaDescription = models.TextField(max_length=150, null=True, blank=True)
    meta_robots = models.CharField(
        max_length=50,
        choices=ROBOTS_CHOICES,
        default='INDEX,FOLLOW',
        verbose_name='وضعیت نمایش در موتورهای جستجو (SEO)',
        help_text='تنظیم کنید که این صفحه در گوگل دیده شود یا خیر'
    )

class TourReview(models.Model):
    """نظر مشتری دربارهٔ تورهای یک کشور.

    نظرات گوگل مپ را نمی‌شود خودکار خواند: Places API حداکثر ۵ نظر می‌دهد،
    اجازهٔ فیلتر کردن بر اساس تور را ندارد و از ایران هم در دسترس نیست. پس
    نظر از گوگل کپی و اینجا ثبت می‌شود و کشورش مشخص می‌گردد تا در صفحهٔ
    تور همان کشور دیده شود.
    """
    SOURCE_CHOICES = [
        ('google', 'گوگل مپ'),
        ('site', 'ثبت‌شده در سایت'),
        ('instagram', 'اینستاگرام'),
        ('other', 'سایر'),
    ]
    RATING_CHOICES = [(i, '%d ستاره' % i) for i in range(1, 6)]

    author = models.CharField(max_length=150, verbose_name='نام نظردهنده')
    rating = models.PositiveSmallIntegerField(
        default=5, choices=RATING_CHOICES, verbose_name='امتیاز')
    text = models.TextField(max_length=1500, verbose_name='متن نظر')
    review_date = models.DateField(
        null=True, blank=True, verbose_name='تاریخ نظر')
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, null=True, blank=True,
        related_name='reviews', verbose_name='مربوط به تورهای کدام کشور')
    source = models.CharField(
        max_length=20, choices=SOURCE_CHOICES, default='google',
        verbose_name='منبع نظر')
    source_url = models.URLField(
        max_length=500, null=True, blank=True,
        verbose_name='لینک اصل نظر (اختیاری)')
    publish = models.BooleanField(default=True, verbose_name='نمایش در سایت')
    sort_order = models.IntegerField(
        default=0, verbose_name='ترتیب نمایش (کوچک‌تر جلوتر)')
    # شناسهٔ یکتای نظر در گوگل (places/X/reviews/Y) تا هر بار
    # دریافت، نظرهای تکراری دوباره ثبت نشوند
    external_id = models.CharField(
        max_length=190, null=True, blank=True, db_index=True,
        verbose_name='شناسهٔ نظر در گوگل')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sort_order', '-review_date', '-created_at']
        verbose_name = 'نظر مشتری'
        verbose_name_plural = 'نظرات مشتریان'

    def __str__(self):
        where = self.country.TitleC if self.country else 'بدون کشور'
        return '%s - %s (%d)' % (self.author, where, self.rating)


class Subscribe(models.Model):
    Mobile = models.CharField(max_length=15)

    def __str__(self):
        return self.Mobile

class Footer(models.Model):
    About = models.TextField(max_length=500)
    Address = models.CharField(max_length=200)
    Phone = models.CharField(max_length=40)
    Email = models.CharField(max_length=100)
    instagram = models.CharField(max_length=200)
    Linkedin = models.CharField(max_length=200)
    Telegram = models.CharField(max_length=200)
    Samandehi = models.CharField(max_length=200)
    Etehadieh = models.CharField(max_length=200)
    PsLaw = models.CharField(max_length=200)
    dollar_rate = models.IntegerField(default=170000, verbose_name='نرخ دلار به تومان')

class TourInterest(models.Model):
    name = models.CharField(max_length=100)
    family = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    page_type = models.CharField(max_length=20, blank=True)
    page_slug = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} {self.family} - {self.phone}"


class TourOrder(models.Model):
    api_partner = models.ForeignKey(
        'ApiPartner', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='orders', verbose_name='ثبت‌شده از طریق آژانس (API)'
    )
    OrderTime = models.DateTimeField(null=True, blank=True)
    OrderTour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    Orderpackage = models.ForeignKey(Package, on_delete=models.CASCADE, null=True, blank=True)
    Name = models.CharField(max_length=300)
    Family = models.CharField(max_length=300)
    Mobile = models.CharField(max_length=15)
    OrderPack = models.CharField(max_length=1000, null=True, blank=True)
    OrderCode = models.CharField(max_length=300, null=True, blank=True)
    adult = models.IntegerField(default=1, null=True, blank=True)
    adult2 = models.IntegerField(default=0, null=True, blank=True)
    chield = models.IntegerField(default=0, null=True, blank=True)
    chield2 = models.IntegerField(default=0, null=True, blank=True)
    infont = models.IntegerField(default=0, null=True, blank=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    View = models.BooleanField(default=False, null=True, blank=True)
    doc1 = models.FileField(upload_to='media/order', null=True, blank=True)
    doc2 = models.FileField(upload_to='media/order', null=True, blank=True)
    doc3 = models.FileField(upload_to='media/order', null=True, blank=True)
    doc4 = models.FileField(upload_to='media/order', null=True, blank=True)
    doc5 = models.FileField(upload_to='media/order', null=True, blank=True)
    doc6 = models.FileField(upload_to='media/order', null=True, blank=True)
    doc7 = models.FileField(upload_to='media/order', null=True, blank=True)
    doc8 = models.FileField(upload_to='media/order', null=True, blank=True)
    doc9 = models.FileField(upload_to='media/order', null=True, blank=True)
    doc10 = models.FileField(upload_to='media/order', null=True, blank=True)
    OrderStat = models.CharField(choices=ORDER_STATUS, max_length=200, null=True, blank=True,
                                 default=ORDER_STATUS[0][0])

    def __str__(self):
        return self.Name + self.Family

class FAQ(models.Model):
    Countryfaq = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    Question = models.CharField(max_length=500, null=True, blank=True)
    Answer = RichTextUploadingField(max_length=10000, null=True, blank=True, config_name='col_lg_6')

class cityFAQ(models.Model):
    Cityfaq = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    Question = models.CharField(max_length=500, null=True, blank=True)
    Answer = RichTextUploadingField(max_length=5000, null=True, blank=True, config_name='col_lg_6')

class OrderDoc(models.Model):
    ordernum = models.ForeignKey(TourOrder, on_delete=models.CASCADE, null=True, blank=True)
    doc1 = models.FileField(upload_to='media/order', null=True, blank=True)
    doc2 = models.FileField(upload_to='media/order', null=True, blank=True)
    doc3 = models.FileField(upload_to='media/order', null=True, blank=True)
    doc4 = models.FileField(upload_to='media/order', null=True, blank=True)
    doc5 = models.FileField(upload_to='media/order', null=True, blank=True)
    doc6 = models.FileField(upload_to='media/order', null=True, blank=True)
    doc7 = models.FileField(upload_to='media/order', null=True, blank=True)
    doc8 = models.FileField(upload_to='media/order', null=True, blank=True)
    doc9 = models.FileField(upload_to='media/order', null=True, blank=True)
    doc10 = models.FileField(upload_to='media/order', null=True, blank=True)

class galleryImg(models.Model):
    image = models.ImageField(upload_to='media/post/main-image')

class faq_home(models.Model):
    question = models.CharField(max_length=500)
    answer = models.TextField(max_length=1000)

class tour_images(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    image = models.FileField(upload_to='tours/', validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif'])])

class spacial_destinations(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    show_homepage = models.BooleanField(default=False)
    show_tourpage = models.BooleanField(default=False)
    homepage_img = ResizedImageField(force_format='WEBP', quality=75, upload_to='media/country-image/homepage', null=True, blank=True)
    homepage_icon = ResizedImageField(force_format='WEBP', quality=75, upload_to='media/country-image/homepage/icon', null=True, blank=True)
    tourpage_img = ResizedImageField(force_format='WEBP', quality=75, upload_to='media/country-image/homepage', null=True, blank=True)
    tourpage_icon = ResizedImageField(force_format='WEBP', quality=75, upload_to='media/country-image/homepage/icon', null=True, blank=True)

class hotel_faq_Country(models.Model):
    Countryfaq = models.ForeignKey("tour.Country", on_delete=models.CASCADE, null=True, blank=True, related_name='faq_country')
    Question = models.CharField(max_length=500, null=True, blank=True)
    Answer = RichTextUploadingField(max_length=10000, null=True, blank=True, config_name='col_lg_6')

class hotel_faq_city(models.Model):
    Cityfaq = models.ForeignKey("tour.City", on_delete=models.CASCADE, null=True, blank=True, related_name='faq_city')
    Question = models.CharField(max_length=500, null=True, blank=True)
    Answer = RichTextUploadingField(max_length=5000, null=True, blank=True, config_name='col_lg_6')

class ApiPartner(models.Model):
    name = models.CharField(max_length=200, verbose_name='نام آژانس / همکار')
    api_key = models.CharField(max_length=64, unique=True, editable=False, verbose_name='کلید API')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    note = models.CharField(max_length=300, null=True, blank=True, verbose_name='توضیحات')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    last_used_at = models.DateTimeField(null=True, blank=True, verbose_name='آخرین استفاده')

    def save(self, *args, **kwargs):
        if not self.api_key:
            self.api_key = secrets.token_hex(24)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'کلید دسترسی API تور'
        verbose_name_plural = 'کلیدهای دسترسی API تور'

