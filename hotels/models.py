from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models
from django_resized import ResizedImageField
from multiselectfield.db.fields import MultiSelectField
from ckeditor_uploader.fields import RichTextUploadingField

RATING = [
    ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')
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

class Hotel_Menu(models.Model):
    MenuTitle = models.CharField(max_length=150)
    MenuDesc = RichTextUploadingField(max_length=3000, null=True, blank=True)
    page_title = models.CharField(max_length=100, null=True, blank=True)
    meta_keywords = models.CharField(max_length=150, null=True, blank=True)
    meta_description = models.TextField(max_length=300, null=True, blank=True)
    slug = models.SlugField(blank=True, null=True)

    def __str__(self):
        return self.MenuTitle


class Hotel_Data(models.Model):
    Creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator')
    HotelName = models.CharField(max_length=500)
    HotelNameEnglish = models.CharField(max_length=500, null=True, blank=True)
    Slug = models.SlugField(null=False, unique=True, max_length=200)
    Hcountry = models.ForeignKey("tour.Country", on_delete=models.CASCADE, default=13, related_name='hotel_country')
    Hcity = models.ForeignKey("tour.City", on_delete=models.CASCADE, default=29, db_index=True, related_name='hotel_city')
    HotelRating = models.CharField(choices=RATING, max_length=1, null=True, blank=True )
    HotelBookingRate = models.CharField(max_length=4, null=True, blank=True )
    HotelTpRate = models.CharField(max_length=4, null=True, blank=True )
    HotelShotDesc = RichTextUploadingField(max_length=1000, null=True, blank=True )
    HotelDesc = RichTextUploadingField(max_length=25000, null=True, blank=True)
    HotelRoom = models.CharField(max_length=100, null=True, blank=True)
    HotelAddress = models.CharField(max_length=1000, null=True, blank=True)
    HotelPhone = models.CharField(max_length=500, null=True, blank=True)
    HotelWebSite = models.CharField(max_length=1000, null=True, blank=True)
    HotelLocation = models.CharField(max_length=500, null=True, blank=True)
    HotelMap = models.CharField(max_length=1500, null=True, blank=True)
    HotelFeature = models.BooleanField(default=False)
    HotelOR = models.BooleanField(default=False)
    HotelBB = models.BooleanField(default=False)
    HotelHB = models.BooleanField(default=False)
    HotelFB = models.BooleanField(default=False)
    HotelAll = models.BooleanField(default=False)
    HotelUall = models.BooleanField(default=False)
    HotelMaxAll = models.BooleanField(default=False)
    HotelService = MultiSelectField(choices=HOTEL_SERVICES, max_length=5000, max_choices=50, null=True, blank=True)
    RoomService = MultiSelectField(choices=ROOM_SERVICES, max_length=800, max_choices=50, null=True, blank=True)
    Service = MultiSelectField(choices=SERVICES, max_length=800, max_choices=50, null=True, blank=True)
    intertainment = MultiSelectField(choices=INTERTAINMENT, max_length=800, max_choices=50, null=True, blank=True)
    HotelImage = ResizedImageField(force_format='WEBP', quality=75, upload_to='hotel-image', null=True, blank=True)
    HotelMenu = models.ForeignKey(Hotel_Menu, on_delete=models.CASCADE, null=True, blank=True)
    metaKeyword = models.TextField(max_length=150, null=True, blank=True)
    metaDescription = models.TextField(max_length=300, null=True, blank=True)
    viewCount = models.IntegerField(default=0, null=True, blank=True)
    htitle = models.CharField(max_length=1000, null=True, blank=True)
    satrap_gte = models.BooleanField(default=False)
    top_rate = models.BooleanField(default=False)
    hotel_price = models.CharField(max_length=40, null=True, blank=True)
    reseve_link = models.CharField(max_length=100, null=True, blank=True)


    def __str__(self):
        DisplayName = str(self.HotelName) + ' - ' + str(self.Hcity)
        return DisplayName

class hotel_images(models.Model):
    hotel = models.ForeignKey(Hotel_Data, on_delete=models.CASCADE, null=True, blank=True)
    image = models.FileField(upload_to='hotels/', validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif'])])

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)

class hotel_comments(models.Model):
    hotel = models.ForeignKey(Hotel_Data, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=300)
    email = models.EmailField()
    desc = models.TextField(max_length=5000)
    create_date = models.DateField(auto_now_add=True, null=True, blank=True)
    publish = models.BooleanField(default=False)
    hotel_rate = models.CharField(max_length=2, null=True, blank=True)

    def __str__(self):
        return self.full_name
