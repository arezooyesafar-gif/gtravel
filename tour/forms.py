from .models import *
from django import forms
from captcha.fields import CaptchaField
from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime,GregorianToJalali


class tour_date_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_date'] = JalaliDateField(widget=AdminJalaliDateWidget)
        self.fields['start_date'].widget.attrs.update({
            'placeholder': ' تاریخ رفت تــور را وارد کنید',
            # 'type':'date'
        })
        self.fields['end_date'] = JalaliDateField(widget=AdminJalaliDateWidget)
        self.fields['end_date'].widget.attrs.update({
            'placeholder': ' تاریخ برگشت تــور را وارد کنید',
            # 'type':'date'
        })
        self.fields['price'].widget.attrs.update({
            'placeholder': ' میزان اختلاف قیمت را وارد کنید',
            'class': 'text-input',
        })
        self.fields['price_type'].widget.attrs.update({
            'class': 'text-input',
        })

    class Meta:
        model = date_plan
        exclude = ['tour']

class TripPlan_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['plan_image'].widget = forms.FileInput(attrs={'class': 'form-control'})
        self.fields['title'].widget.attrs.update({
            'class': "text-input",
        })
        self.fields['location'].widget.attrs.update({
            'class': "text-input",
        })
        self.fields['views'].widget.attrs.update({
            'class': "text-input",
        })
        self.fields['services'].widget.attrs.update({
            'class': "text-input",
        })
        self.fields['description'].widget.attrs.update({
            'class': "text-input",
        })

    class Meta:
        model = TripPlan
        exclude = ['tour']

class spacial_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['homepage_img'].widget = forms.FileInput(attrs={'class': 'form-control'})
        self.fields['tourpage_img'].widget = forms.FileInput(attrs={'class': 'form-control'})
        self.fields['tourpage_icon'].widget = forms.FileInput(attrs={'class': 'form-control'})
        self.fields['homepage_icon'].widget = forms.FileInput(attrs={'class': 'form-control'})

    class Meta:
        model = spacial_destinations
        exclude = ['country', 'city']

class uploadimgForm(forms.Form):
    file = forms.FileField()


class CurrencyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Title'].widget.attrs.update({
                'placeholder': '',
                'class': 'text-input',
            })
    class Meta:
        model = Currency
        fields = '__all__'


class CreateCountryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Flagimg'].widget = forms.FileInput(attrs={'class': 'input-text hide-field'})
        self.fields['country_iamge'].widget = forms.FileInput(attrs={'class': ''})
        self.fields['country_icon'].widget = forms.FileInput(attrs={'class': ''})
        self.fields['TitleC'].widget.attrs.update({
                'placeholder': '',
                'class': 'text-input',
            })
        self.fields['tourmk'].widget.attrs.update({
                'placeholder': '',
                'class': 'text-input',
            })
        self.fields['tourmd'].widget.attrs.update({
                'placeholder': '',
                'class': 'text-input',
            })
        self.fields['hotelmk'].widget.attrs.update({
                'placeholder': '',
                'class': 'text-input',
            })
        self.fields['hotelmd'].widget.attrs.update({
                'placeholder': '',
                'class': 'text-input',
            })
        self.fields['tltitle'].widget.attrs.update({
                'placeholder': '',
                'class': 'text-input',
            })
        self.fields['hltitle'].widget.attrs.update({
                'placeholder': '',
                'class': 'text-input',
            })
        self.fields['slug'].widget.attrs.update({
                'placeholder': '',
                'class': 'text-input',
            })
        self.fields['showInMenu'].widget.attrs.update({
                'placeholder': '',
                'class': 'text-input',
            })
        self.fields['Description'].widget.attrs.update({
                'placeholder': '',
            })
        self.fields['menu_position'].widget.attrs.update({
            'id': 'id_Tcountry',
            'class': 'text-input',
        })
        self.fields['menu_order'].widget.attrs.update({
            'class': 'text-input',
        })
    class Meta:
        model = Country
        fields = '__all__'


class CreateCityForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cityImg'].widget = forms.FileInput(attrs={'class': 'input-text hide-field'})
        self.fields['cityIcon'].widget = forms.FileInput(attrs={'class': 'input-text'})
        self.fields['Name'].widget.attrs.update({
                'placeholder': '',
                'class': 'text-input',
            })
        self.fields['CountryName'].widget.attrs.update({
                'placeholder': '',
                'class': 'text-input',
            })
        self.fields['tourmk'].widget.attrs.update({
                'placeholder': '',
                'class': 'text-input',
            })
        self.fields['tourmd'].widget.attrs.update({
                'placeholder': '',
                'class': 'text-input',
            })
        self.fields['hotelmk'].widget.attrs.update({
                'placeholder': '',
                'class': 'text-input',
            })
        self.fields['hotelmd'].widget.attrs.update({
                'placeholder': '',
                'class': 'text-input',
            })
        self.fields['tltitle'].widget.attrs.update({
                'placeholder': '',
                'class': 'text-input',
            })
        self.fields['hltitle'].widget.attrs.update({
                'placeholder': '',
                'class': 'text-input',
            })
        self.fields['showInMenu'].widget.attrs.update({
                'placeholder': '',
                'class': 'text-input',
            })
        self.fields['Description'].widget.attrs.update({
                'placeholder': '',
                'class': 'text-input',
            })
        self.fields['slug'].widget.attrs.update({
                'placeholder': '',
                'class': 'text-input',
            })
    class Meta:
        model = City
        fields = '__all__'


class SearchForm(forms.Form):
    COUNT = [
        ('', 'انتخاب تعداد شب های اقامت'),
        ('1', '1'),('2', '2'),('3', '3'),('4', '4'),('5', '5'),('6', ''),
    ]
    DestCountry = forms.CharField(max_length=300, required=False)
    NightCount = forms.CharField(max_length=300, required=False)
    StartDate = forms.DateField(widget=AdminJalaliDateWidget(), required=False)

    DestCountry.widget.attrs.update({
        'class': 'text-input search-input',
        'placeholder': ' مقصد را وارد کنید',
        'onchange': 'hide_search_box()',
        'autocomplete': 'off'
    })
    NightCount.widget.attrs.update({
        'class': 'text-input search-input',
        'placeholder': 'تعداد شب های اقامت را وارد کنید',
        'step': '1',
        'min': '1',
        'value' : '1',
        'onkeypress': 'return isNumberKey(event)s'
    })
    StartDate.widget.attrs.update({
        'placeholder': 'تاریخ رفت را انتخاب کنید',
        'autocomplete': 'off'
    })

class tour_search_form(forms.Form):
    tour_name = forms.CharField(max_length=300, required=False)
    start_date = forms.DateField(widget=AdminJalaliDateWidget(), required=False)
    end_date = forms.DateField(widget=AdminJalaliDateWidget(), required=False)

    tour_name.widget.attrs.update({
        'class': 'text-input search-input',
        'placeholder': ' نام تور را وارد کنید'
    })
    start_date.widget.attrs.update({
        'placeholder': 'تاریخ رفت',
        'autocomplete': 'off',
        'onchange': 'resetStartdate()'
    })
    end_date.widget.attrs.update({
        'placeholder': 'تاریخ برگشت',
        'autocomplete': 'off',
        'onchange':"resetEnddate()"
    })

class hotel_search_form(forms.Form):
    hotel_name = forms.CharField(max_length=300, required=False)
    hotel_name_eng = forms.CharField(max_length=300, required=False)

    hotel_name.widget.attrs.update({
        'class': 'text-input search-input',
        'placeholder': ' نام هتل را وارد کنید'
    })
    hotel_name_eng.widget.attrs.update({
        'placeholder': 'نام انگلیسی هتل را انتخاب کنید',
        'autocomplete': 'off',
        'class': 'text-input search-input',
        # 'onchange': 'convertDateadmin()'
    })


class CreateAirLineForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['AirlineLogo'].widget = forms.FileInput(attrs={'class': 'input-text hide-field'})
        self.fields['AirLineTitle'].widget.attrs.update({
            'class': 'air-line-name',
            'id': 'Air-Line-Name',
            # 'placeholder': ' نام ایرلاین را وارد کنید'
        })
        self.fields['AirLineTitle'].widget.attrs.update(
            {
                # 'placeholder': 'نام ایرلاین را وارد کنید',
                'class': 'text-input',
            }
        )
        self.fields['AirlineCargo'].widget.attrs.update(
            {
                # 'placeholder': 'نام ایرلاین را وارد کنید',
                'class': 'text-input',
            }
        )

    
    class Meta:
        model = AirLineData
        exclude = ['Creator', 'Slug']

class CreateAirPortForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['AirportEn'].widget.attrs.update(
            {
                'placeholder': '',
                'class': 'text-input',
            }
        )
        self.fields['AirportFa'].widget.attrs.update(
            {
                'placeholder': '',
                'class': 'text-input',
            }
        )

    class Meta:
        model = Airport
        fields = '__all__'


class TourCityForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['CyName'].widget.attrs.update({
                'placeholder': '',
                'class': 'text-input',
            })
        self.fields['CtName'].widget.attrs.update({
                'placeholder': '',
                'class': 'text-input',
            })
        self.fields['Airline'].widget.attrs.update({
                'placeholder': '',
                'class': 'text-input',
            })
        self.fields['FromAirport'].widget.attrs.update({
                'placeholder': '',
                'class': 'text-input',
            })
        self.fields['ToAirport'].widget.attrs.update({
                'placeholder': '',
                'class': 'text-input',
            })
        self.fields['FlightTime'].widget.attrs.update({
                'placeholder': '',
                'class': 'text-input',
            })
        self.fields['FlightDuration'].widget.attrs.update({
                'placeholder': '',
                'class': 'text-input',
            })
        self.fields['FlightClass'].widget.attrs.update({
                'placeholder': '',
                'class': 'text-input',
            })
        self.fields['NightCount'].widget.attrs.update({
                'placeholder': '',
                'class': 'text-input',
            })
        self.fields['Waiting'].widget.attrs.update({
                'placeholder': '',
                'class': 'text-input',
            })
        self.fields['GDest'].widget.attrs.update({
                'placeholder': '',
                'class': 'text-input',
            })
        self.fields['GTransfer'].widget.attrs.update({
                'placeholder': '',
                'class': 'text-input',
            })
        self.fields['QTransfer'].widget.attrs.update({
            'placeholder': '',
            'class': 'text-input',
        })
        self.fields['flight_return'].widget.attrs.update({
            'placeholder': '',
            'class': 'text-input',
        })

    class Meta:
        model = TourCity
        exclude = ['TourName']


class CreateTourForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CreateTourForm, self).__init__(*args, **kwargs)
        self.fields['origin_city'].required = False
        self.fields['TourImage'].widget = forms.FileInput(attrs={'class': 'input-text hide-field'})
        self.fields['tour_main'].widget = forms.FileInput(attrs={'class': 'input-text hide-field'})
        self.fields['Title'].widget.attrs.update({
            'class': 'text-input',
            'placeholder': ' نام تــور را وارد کنید'
        })
        self.fields['StartDate'] = JalaliDateField(widget=AdminJalaliDateWidget)
        self.fields['StartDate'].widget.attrs.update({
            'type': 'date',
            'placeholder': ' تاریخ شروع تــور را وارد کنید'
        })
        self.fields['EndDate'] = JalaliDateField(widget=AdminJalaliDateWidget)
        self.fields['EndDate'].widget.attrs.update({
            'type': 'date',
            'placeholder': ' تاریخ اتمام تــور را وارد کنید'
        })
        self.fields['NightCount'].widget.attrs.update({
            'class': 'text-input',
            'placeholder': ' تعداد شب های اقامت را وارد کنید'
        })
        self.fields['DayCount'].widget.attrs.update({
            'class': 'text-input',
            'placeholder': ' تعداد روزهای اقامت را وارد کنید'
        })
        self.fields['TourImage'].widget.attrs.update({
            'class': 'text-input hide-field'
        })
        self.fields['Offer'].widget.attrs.update({
            'class': 'text-input'
        })
        self.fields['Slug'].widget.attrs.update({
            'class': 'text-input'
        })
        self.fields['TourMenu'].widget.attrs.update({
            'class': 'text-input'
        })
        self.fields['Tcountry'].widget.attrs.update({
            'class': 'text-input'
        })
        self.fields['Tcity'].widget.attrs.update({
            'class': 'text-input'
        })
        self.fields['origin_city'].widget.attrs.update({
            'class': 'text-input'
        })
        self.fields['ShortDsc'].widget.attrs.update({
            'class': 'text-input'
        })
        self.fields['pdfdesc'].widget.attrs.update({
            'class': 'text-input',
            'width': '600px',
            'rows': '2'
        })
        self.fields['MetaDescription'].widget.attrs.update({
            'class': 'text-input',
            'width': '600px',
            'rows': '2'
        })
        self.fields['MetaKeywords'].widget.attrs.update({
            'class': 'text-input',
            'width': '600px',
            'rows': '2'
        })
        self.fields['Description'].widget.attrs.update({
            'class': 'text-input'
        })
        self.fields['OfferShow'].widget.attrs.update({

        })
        self.fields['tstitle'].widget.attrs.update({
            'class': 'text-input'
        })
        self.fields['spacial_lable'].widget.attrs.update({
            'class': 'text-input'
        })
        self.fields['add_peice_single'].widget.attrs.update({
            'class': 'text-input',
        })
        self.fields['add_peice_dubel'].widget.attrs.update({
            'class': 'text-input',
        })
        self.fields['add_peice_with_bed'].widget.attrs.update({
            'class': 'text-input',
        })
        self.fields['add_peice_without_bed'].widget.attrs.update({
            'class': 'text-input',
        })
        self.fields['add_peice_infont'].widget.attrs.update({
            'class': 'text-input',
        })
        self.fields['TourPdf'].widget = forms.FileInput(attrs={'class': 'input-text hide-field'})

    class Meta:
        model = Tour
        exclude = ['Creator', 'updateDate']


class CreatePackageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['PackageName'].widget.attrs.update({
            'class': 'text-input'
        })
    class Meta:
        model = MainPackage
        exclude = ['Creator']


class AddToPackageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['MainPkg'].empty_label = 'پکیج را انتخاب کنبد'
        self.fields['MainPkg'].widget.attrs.update({
            'class': 'text-input'
        })
        self.fields['SingleBedPrice'].widget.attrs.update({
            'class': 'text-input'
        })
        self.fields['DoubleBedPrice'].widget.attrs.update({
            'class': 'text-input',
            'onkeypress': 'seprateNum()'
        })
        self.fields['BabyWithBedPrice'].widget.attrs.update({
            'class': 'text-input'
        })
        self.fields['BabyWithoutBedPrice'].widget.attrs.update({
            'class': 'text-input'
        })
        self.fields['InfontPrice'].widget.attrs.update({
            'class': 'text-input'
        })
        self.fields['SingleBedPrice_doller'].widget.attrs.update({
            'class': 'text-input'
        })
        self.fields['DoubleBedPrice_doller'].widget.attrs.update({
            'class': 'text-input',
            'onkeypress': 'seprateNum()'
        })
        self.fields['BabyWithBedPrice_doller'].widget.attrs.update({
            'class': 'text-input'
        })
        self.fields['BabyWithoutBedPrice_doller'].widget.attrs.update({
            'class': 'text-input'
        })
        self.fields['InfontPrice_doller'].widget.attrs.update({
            'class': 'text-input'
        })
        self.fields['DollerPrice'].widget.attrs.update({
            'class': 'text-input'
        })
        self.fields['Pcry'].widget.attrs.update({
            'class': 'text-input'
        })
        self.fields['fr_Pcry'].widget.attrs.update({
            'class': 'text-input'
        })
        self.fields['view'].widget.attrs.update({
            'class': 'text-input select-view'
        })
        self.fields['view_hotel'].widget.attrs.update({
            'class': 'text-input select-view'
        })
        self.fields['view_mhotel'].widget.attrs.update({
            'class': 'text-input select-view'
        })
        self.fields['view_m1hotel'].widget.attrs.update({
            'class': 'text-input select-view'
        })
        self.fields['view_m2hotel'].widget.attrs.update({
            'class': 'text-input select-view'
        })
        self.fields['view_m3hotel'].widget.attrs.update({
            'class': 'text-input select-view'
        })
        self.fields['view_m4hotel'].widget.attrs.update({
            'class': 'text-input select-view'
        })
        self.fields['service_hotel'].widget.attrs.update({
            'class': 'text-input select-view'
        })
        self.fields['service_mhotel'].widget.attrs.update({
            'class': 'text-input select-view'
        })
        self.fields['service_m1hotel'].widget.attrs.update({
            'class': 'text-input select-view'
        })
        self.fields['service_m2hotel'].widget.attrs.update({
            'class': 'text-input select-view'
        })
        self.fields['service_m3hotel'].widget.attrs.update({
            'class': 'text-input select-view'
        })
        self.fields['service_m4hotel'].widget.attrs.update({
            'class': 'text-input select-view'
        })

    class Meta:
        model = Package
        exclude = ['Creator', 'Slug', 'TourName',
        'HotelName', 'Mhotel', 'M1hotel', 'M2hotel', 'M3hotel']





class TourMenuForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['MenuTitle'].widget.attrs.update({
            'class': 'text-input'
        })
        self.fields['page_title'].widget.attrs.update({
            'class': 'text-input'
        })
        self.fields['meta_keywords'].widget.attrs.update({
            'class': 'text-input'
        })
        self.fields['meta_description'].widget.attrs.update({
            'class': 'text-input',
            'rows': '2'
        })
        self.fields['slug'].widget.attrs.update({
            'class': 'text-input',
            'placeholder': 'به انگلیسی وارد کنید'
        })
        self.fields['MenuDesc'].widget.attrs.update({
            'class': 'text-input',
            'placeholder': 'توضيحات منو را وارد کنيد'
        })

    class Meta:
        model = TourMenu
        fields = '__all__'





class ContactUsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['FirstName'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': ' نام را وارد کنيد '
        })
        self.fields['LastName'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': ' نام خانوادگي را وارد کنيد '
        })
        self.fields['Mobile'].widget.attrs.update({
            'class': 'form-control mobile-us',
            'placeholder': ' موبايل را وارد کنيد '
        })
        self.fields['Message'].widget.attrs.update(
            {
                'placeholder': 'پيام خود را وارد کنيد',
                'class': 'form-control',
                'rows': '5',
            }
        )

    class Meta:
        model = ContactUs
        fields = '__all__'

class AboutUsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['TextAbout'].widget.attrs.update({
            'class': 'text-input',
            'placeholder': ' متن درباره ما را وارد کنيد '
        })

    class Meta:
        model = AboutUs
        fields = '__all__'

class ContactUsTextForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['TextContact'].widget.attrs.update({
            'class': 'text-input',
            'placeholder': 'متن تماس با ما را وارد کنيد'
        })

    class Meta:
        model = ContactUsText
        fields = '__all__'

class SlideshowCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['FirstImage'].widget = forms.FileInput(attrs={'class': 'input-text hide-field'})
        self.fields['SeconedImage'].widget = forms.FileInput(attrs={'class': 'input-text hide-field'})
        self.fields['ThiredImage'].widget = forms.FileInput(attrs={'class': 'input-text hide-field'})
       
        
    class Meta:
        model = SlideShow
        fields = '__all__'

class PMemoriesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Name'].widget.attrs.update({
            'class': 'text-input',
            'placeholder': 'نام خود را وارد کنيد'
        })
        self.fields['headline'].widget.attrs.update({
            'class': 'text-input',
        })
        self.fields['Family'].widget.attrs.update({
            'class': 'text-input',
            'placeholder': 'نام خانوادگي خود را وارد کنيد'
        })
        self.fields['Mobile'].widget.attrs.update({
            'class': 'text-input memo',
            'placeholder': 'موبايل خود را وارد کنيد'
        })
        self.fields['Email'].widget.attrs.update({
            'class': 'text-input',
            'placeholder': 'آدرس ايميل را وارد کنيد'
        })
        self.fields['img1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder':''
        })
        self.fields['img2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': ''
        })
        self.fields['Message'].widget.attrs.update({
            'class': 'text-input',
            'cols': '102',
            'id': 'memori-message',
            'placeholder': 'خاطرات سفر '
        })
        self.fields['publish'].widget.attrs.update({
            'class': 'text-input',
        })
        self.fields['category'].widget.attrs.update({
            'class': 'text-input',
        })
        self.fields['meta_robots'].widget.attrs.update({
            'class': 'text-input',
        })
        
    class Meta:
        model = PMemories
        exclude = ['created_date']


class CreateMemoryCategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['CatName'].widget.attrs.update({
            'class': 'text-input',
            'placeholder': ' نام دسته بندی را وارد کنید',
        })
        self.fields['parentCat'].widget.attrs.update({
            'class': 'text-input',
            'placeholder': ' نام دسته بندی را وارد کنید',
        })
        self.fields['slug'].widget.attrs.update({
            'class': 'text-input',

        })
        self.fields['page_title'].widget.attrs.update({
            'class': 'text-input',

        })
        self.fields['meta_desc'].widget.attrs.update({
            'class': 'text-input',

        })
        self.fields['meta_keyword'].widget.attrs.update({
            'class': 'text-input',

        })

    class Meta:
        model = MemoryCategory
        fields = '__all__'


class SubscribeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Mobile'].widget.attrs.update({
            'class': 'subscribe',
            'placeholder': 'شماره موبايل جهت عضويت در خبرنامه',
            'onkeypress':"return isNumber(event)",
            'pattern': "09(0[1-2]|1[0-9]|3[0-9]|2[0-1])-?[0-9]{3}-?[0-9]{4}",
        })
        
    class Meta:
        model = Subscribe
        fields = '__all__'

class relatedCityForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['country'].empty_label = 'کشور مورد نظر را انتخاب کنید'
        self.fields['country'].empty_label = 'شهر مورد نظر را انتخاب کنید'
        self.fields['country'].widget.attrs.update({
            'class': 'form-select',
            'onchange': 'getCityList()'
        })
        self.fields['city'].widget.attrs.update({
            'class': 'form-select',
        })

    class Meta:
        model = related_tour_city
        exclude = ['tour']


class reservsionCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Name'].widget.attrs.update({
            'class': 'form-control reserve',
            'placeholder': 'نام '
        })
        self.fields['Family'].widget.attrs.update({
            'class': 'form-control reserve',
            'placeholder': 'نام خانوادگي'
        })
        self.fields['Mobile'].widget.attrs.update({
            'class': 'form-control reserve',
            'placeholder': 'شماره موبايل',
            'onkeypress':"return isNumber(event)",
            'pattern': "09(0[1-2]|1[0-9]|3[0-9]|2[0-1])-?[0-9]{3}-?[0-9]{4}",
        })
        self.fields['adult'].widget.attrs.update({
            'class': 'form-control reserve',
            'onchange': 'calculateprice()'
        })
        self.fields['adult2'].widget.attrs.update({
            'class': 'form-control reserve',
            'onchange': 'calculateprice()'
        })
        self.fields['chield'].widget.attrs.update({
            'class': 'form-control reserve',
            'onchange': 'calculateprice()'
        })
        self.fields['chield2'].widget.attrs.update({
            'class': 'form-control reserve',
            'onchange': 'calculateprice()'
        })
        self.fields['infont'].widget.attrs.update({
            'class': 'form-control reserve',
            'onchange': 'calculateprice()'
        })
        self.fields['description'].widget.attrs.update({
            'class': 'form-control reserve',
            'rows': '5'
        })
    class Meta:
        model = TourOrder
        exclude = ['OrderTour', 'OrderTime', 'view', 'Orderpackage']

class orderUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Orderpackage'].disabled = True
        self.fields['OrderTour'].disabled = True
        self.fields['Name'].widget.attrs.update({
            'class': 'text-input reserve',
            'placeholder': 'نام '
        })
        self.fields['Family'].widget.attrs.update({
            'class': 'text-input reserve',
            'placeholder': 'نام خانوادگي'
        })
        self.fields['Mobile'].widget.attrs.update({
            'class': 'text-input reserve',
            'placeholder': 'شماره موبايل'
        })
        self.fields['OrderTour'].widget.attrs.update({
            'class': 'text-input reserve',
        })
        self.fields['Orderpackage'].widget.attrs.update({
            'class': 'text-input reserve',

        })
        self.fields['OrderPack'].widget.attrs.update({
            'class': 'text-input reserve',
        })
        self.fields['OrderCode'].widget.attrs.update({
            'class': 'text-input reserve',
        })
        self.fields['adult'].widget.attrs.update({
            'class': 'text-input reserve',
            'onchange': 'calculateprice()'
        })
        self.fields['adult2'].widget.attrs.update({
            'class': 'text-input reserve',
            'onchange': 'calculateprice()'
        })
        self.fields['chield'].widget.attrs.update({
            'class': 'text-input reserve',
            'onchange': 'calculateprice()'
        })
        self.fields['chield2'].widget.attrs.update({
            'class': 'text-input reserve',
            'onchange': 'calculateprice()'
        })
        self.fields['infont'].widget.attrs.update({
            'class': 'text-input reserve',
            'onchange': 'calculateprice()'
        })
        self.fields['description'].widget.attrs.update({
            'class': 'text-input reserve',
            'rows': '2'
        })
        self.fields['OrderStat'].widget.attrs.update({
            'class': 'text-input reserve',
        })
        self.fields['View'].widget.attrs.update({
            'class': 'text-input reserve',
        })
        self.fields['OrderTime'].widget.attrs.update({
            'class': 'text-input reserve',
        })
        self.fields['doc1'].widget.attrs.update({
            'class': 'text-input reserve',
        })
        self.fields['doc2'].widget.attrs.update({
            'class': 'text-input reserve',
        })
        self.fields['doc3'].widget.attrs.update({
            'class': 'text-input reserve',
        })
        self.fields['doc4'].widget.attrs.update({
            'class': 'text-input reserve',
        })
        self.fields['doc5'].widget.attrs.update({
            'class': 'text-input reserve',
        })
        self.fields['doc6'].widget.attrs.update({
            'class': 'text-input reserve',
        })
        self.fields['doc7'].widget.attrs.update({
            'class': 'text-input reserve',
        })
        self.fields['doc8'].widget.attrs.update({
            'class': 'text-input reserve',
        })
        self.fields['doc9'].widget.attrs.update({
            'class': 'text-input reserve',
        })
        self.fields['doc10'].widget.attrs.update({
            'class': 'text-input reserve',
        })
        
    class Meta:
        model = TourOrder
        fields = '__all__'

class FooterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['About'].widget.attrs.update({
            'class': 'text-input',
        })
        self.fields['Address'].widget.attrs.update({
            'class': 'text-input',
        })
        self.fields['Phone'].widget.attrs.update({
            'class': 'text-input',
        })
        self.fields['Email'].widget.attrs.update({
            'class': 'text-input',
        })
        self.fields['instagram'].widget.attrs.update({
            'class': 'text-input',
        })
        self.fields['Linkedin'].widget.attrs.update({
            'class': 'text-input',
        })
        self.fields['Telegram'].widget.attrs.update({
            'class': 'text-input',
        })
        self.fields['Samandehi'].widget.attrs.update({
            'class': 'text-input',
        })
        self.fields['Etehadieh'].widget.attrs.update({
            'class': 'text-input',
        })
        self.fields['PsLaw'].widget.attrs.update({
            'class': 'text-input',
        })
        
    class Meta:
        model = Footer
        fields = '__all__'



class faqCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Question'].widget.attrs.update({
            'class': 'text-input reserve',
            'placeholder': 'متن سوال'
        })
        self.fields['Answer'].widget.attrs.update({
            ##'class': 'text-input reserve',
            ##'placeholder': 'متن پاسخ'
        })
        
    class Meta:
        model = FAQ
        exclude = ['Countryfaq']


class faqhotelcountryCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Question'].widget.attrs.update({
            'class': 'text-input reserve',
            'placeholder': 'متن سوال'
        })
        self.fields['Answer'].widget.attrs.update({
            ##'class': 'text-input reserve',
            ##'placeholder': 'متن پاسخ'
        })

    class Meta:
        model = hotel_faq_Country
        exclude = ['Countryfaq']
class cityfaqCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Question'].widget.attrs.update({
            'class': 'text-input reserve',
            'placeholder': 'متن سوال'
        })
        self.fields['Answer'].widget.attrs.update({
            ##'class': 'text-input reserve',
            'placeholder': 'متن پاسخ'
        })
        
    class Meta:
        model = cityFAQ
        exclude = ['Cityfaq']


class cityfaqhotelCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Question'].widget.attrs.update({
            'class': 'text-input reserve',
            'placeholder': 'متن سوال'
        })
        self.fields['Answer'].widget.attrs.update({
            ##'class': 'text-input reserve',
            'placeholder': 'متن پاسخ'
        })

    class Meta:
        model = hotel_faq_city
        exclude = ['Cityfaq']


class CityCountryMediaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file'].widget = forms.FileInput(attrs={'class': 'input-text hide-field'})
        self.fields['title'].widget.attrs.update({
            'class': 'text-input',
            'placeholder': ' عنوان رسانه را وارد کنید'
        })
        self.fields['thumbnail'].widget = forms.FileInput(attrs={'class': 'input-text hide-field'})

        self.fields['media_type'].widget.attrs.update({
            'class': 'text-input'
        })
    class Meta:
        model = CityCountryMedia
        fields = ['title', 'media_type', 'file', 'thumbnail', 'duration_seconds', 'sort_order', 'is_active']


class createOrderDoc(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['doc1'].widget.attrs.update({
            'class': 'image-input',
        })
        self.fields['doc2'].widget.attrs.update({
            'class': 'image-input',
        })
        self.fields['doc3'].widget.attrs.update({
            'class': 'image-input',
        })
        self.fields['doc4'].widget.attrs.update({
            'class': 'image-input',
        })
        self.fields['doc5'].widget.attrs.update({
            'class': 'image-input',
        })
        self.fields['doc6'].widget.attrs.update({
            'class': 'image-input',
        })
        self.fields['doc7'].widget.attrs.update({
            'class': 'image-input',
        })
        self.fields['doc8'].widget.attrs.update({
            'class': 'image-input',
        })
        self.fields['doc9'].widget.attrs.update({
            'class': 'image-input',
        })
        self.fields['doc10'].widget.attrs.update({
            'class': 'image-input',
        })
        
    class Meta:
        model = OrderDoc
        exclude = ['ordernum']


class create_faq__home_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['answer'].widget.attrs.update({
            'class': 'text-input',
            'cols': '126',
            'rows': '5',
            'placeholder': 'متن جواب را وارد کنید',
        })
        self.fields['question'].widget.attrs.update({
            'class': 'text-input',
            'placeholder': 'متن سوال را وارد کنید',
        })

    class Meta:
        model = faq_home
        fields = "__all__"
