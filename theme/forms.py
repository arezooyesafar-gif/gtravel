from django import forms
from .models import *

class update_main_page(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['st_title'].widget.attrs.update({
            'class': 'text-input',
            'placeholder': '',
        })
        self.fields['about_title'].widget.attrs.update({
            'class': 'text-input',
            'placeholder': '',
        })
        self.fields['about_address'].widget.attrs.update({
            'class': 'text-input',
            'placeholder': '',
        })
        self.fields['about_phone'].widget.attrs.update({
            'class': 'text-input',
            'placeholder': '',
        })
        self.fields['about_text'].widget.attrs.update({
            'class': 'text-input',
            'cols': '126',
            'placeholder': '',
        })
        self.fields['google_review_url'].widget.attrs.update({
            'class': 'text-input',
            'dir': 'ltr',
            'placeholder': 'https://search.google.com/local/writereview?placeid=...',
        })
        for name in ('google_place_id', 'google_places_key', 'google_api_proxy'):
            self.fields[name].widget.attrs.update({
                'class': 'text-input',
                'dir': 'ltr',
            })
        self.fields['google_place_id'].widget.attrs['placeholder'] = 'ChIJ...'
        self.fields['google_places_key'].widget.attrs['placeholder'] = 'AIza...'
        self.fields['google_api_proxy'].widget.attrs['placeholder'] = 'http://127.0.0.1:10809'
        self.fields['blog_title'].widget.attrs.update({
            'class': 'text-input',
            'placeholder': '',
        })
        self.fields['faq_title'].widget.attrs.update({
            'class': 'text-input',
            'placeholder': '',
        })
        self.fields['box_1_title'].widget.attrs.update({
            'class': 'text-input',
            'placeholder': '',
        })
        self.fields['box_2_title'].widget.attrs.update({
            'class': 'text-input',
            'placeholder': '',
        })
        self.fields['box_3_title'].widget.attrs.update({
            'class': 'text-input',
            'placeholder': '',
        })
        self.fields['box_1_desc'].widget.attrs.update({
            'class': 'text-input',
            'placeholder': '',
        })
        self.fields['box_2_desc'].widget.attrs.update({
            'class': 'text-input',
            'placeholder': '',
        })
        self.fields['box_3_desc'].widget.attrs.update({
            'class': 'text-input',
            'placeholder': '',
        })
        self.fields['footer_phone'].widget.attrs.update({
            'class': 'text-input',
            'placeholder': '',
        })
        self.fields['footer_address'].widget.attrs.update({
            'class': 'text-input',
            'placeholder': '',
        })
        self.fields['about_logo'].widget.attrs.update({
            'class': 'text-input',
            'placeholder': '',
        })

    class Meta:
        model = index_page
        fields = "__all__"