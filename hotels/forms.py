from captcha.fields import CaptchaField
from .models import *
from django import forms

class CreateHotelMenuForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['MenuTitle'].widget.attrs.update(
            {
                'placeholder': '',
                'class': 'text-input',
            }
        )
        self.fields['slug'].widget.attrs.update(
            {
                'placeholder': '',
                'class': 'text-input',
            }
        )
        self.fields['MenuDesc'].widget.attrs.update(
            {
                'placeholder': '',
                'class': 'text-input',
            }
        )

    class Meta:
        model = Hotel_Menu
        fields = '__all__'


class CreateHotelMenuForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['MenuTitle'].widget.attrs.update(
            {
                'placeholder': '',
                'class': 'text-input',
            }
        )
        self.fields['slug'].widget.attrs.update(
            {
                'placeholder': '',
                'class': 'text-input',
            }
        )
        self.fields['MenuDesc'].widget.attrs.update(
            {
                'placeholder': '',
                'class': 'text-input',
            }
        )

    class Meta:
        model = Hotel_Menu
        fields = '__all__'

class CreateHotelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['HotelMenu'].empty_label = 'منو هتل را انتخاب کنید'
        self.fields['HotelImage'].widget = forms.FileInput(attrs={'class': 'input-text hide-field'})
        self.fields['HotelService'].widget.attrs.update({
            'class': 'inline-checkbox'
        })
        self.fields['RoomService'].widget.attrs.update({
            'class': 'inline-checkbox room_service'
        })
        self.fields['Service'].widget.attrs.update({
            'class': 'inline-checkbox service'
        })
        self.fields['intertainment'].widget.attrs.update({
            'class': 'inline-checkbox intertainment'
        })
        self.fields['HotelMenu'].widget.attrs.update({
            'class': 'text-input',
        })
        self.fields['HotelName'].widget.attrs.update({
            'class': 'text-input',
            # 'placeholder': ' نام هتل را وارد کنید'
        })
        self.fields['htitle'].widget.attrs.update({
            'class': 'text-input',
            # 'placeholder': ' عنوان صفحه هتل را وارد کنید'
        })
        self.fields['HotelNameEnglish'].widget.attrs.update({
            'class': 'text-input',
            # 'placeholder': ' نام انگلیسی هتل را وارد کنید'
        })
        self.fields['HotelRating'].widget.attrs.update({
            'class': 'text-input',
            # 'placeholder': ' تعداد ستاره هتل را وارد کنید'
        })
        self.fields['HotelBookingRate'].widget.attrs.update({
            'class': 'text-input',
            # 'placeholder': ' امتیاز هتل در سایت بوکینگ را وارد کنید'
        })
        self.fields['HotelTpRate'].widget.attrs.update({
            'class': 'text-input',
            # 'placeholder': ' امتیاز هتل در سایت بوکینگ را وارد کنید'
        })
        self.fields['HotelRoom'].widget.attrs.update({
            'class': 'text-input',
        })
        self.fields['HotelAddress'].widget.attrs.update({
            'class': 'text-input',
        })
        self.fields['HotelPhone'].widget.attrs.update({
            'class': 'text-input',
        })
        self.fields['HotelWebSite'].widget.attrs.update({
            'class': 'text-input',
        })
        self.fields['HotelLocation'].widget.attrs.update({
            'class': 'text-input',
        })
        self.fields['HotelMap'].widget.attrs.update({
            'class': 'text-input',
        })
        self.fields['Hcountry'].widget.attrs.update({
            'class': 'text-input',
        })
        self.fields['Hcity'].widget.attrs.update({
            'class': 'text-input',
        })
        self.fields['metaKeyword'].widget.attrs.update({
            'class': 'text-input',
            'rows': '3'
        })
        self.fields['metaDescription'].widget.attrs.update({
            'class': 'text-input',
            'rows': '3'
        })
        self.fields['hotel_price'].widget.attrs.update({
            'class': 'text-input',
        })
        self.fields['reseve_link'].widget.attrs.update({
            'class': 'text-input',
        })
        self.fields['Slug'].widget.attrs.update({
            'class': 'text-input',
        })
        self.fields['meta_robots'].widget.attrs.update({
            'class': 'text-input',
        })

    def clean(self):
        cleaned_data = super().clean()
        for name in ('HotelService', 'RoomService', 'Service', 'intertainment'):
            values = cleaned_data.get(name) or []
            paid = {value[:-len(PAID_SUFFIX)] for value in values if value.endswith(PAID_SUFFIX)}
            cleaned_data[name] = [value for value in values if value not in paid]
        return cleaned_data

    class Meta:
        model = Hotel_Data
        exclude = ['Creator']


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

class hotel_comment_form(forms.ModelForm):
    captcha = CaptchaField()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['full_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': ' نام و نام خانوادگی را وارد کنید',
        })
        self.fields['email'].widget.attrs.update(
            {
                'placeholder': 'ایمیل را وارد کنید',
                'class': 'form-control',
            }
        )
        self.fields['desc'].widget.attrs.update(
            {
                'placeholder': 'توضیحات را وارد کنید',
                'class': 'form-control',
                'rows': '3'
            }
        )
    class Meta:
        model = hotel_comments
        exclude = ['hotel']