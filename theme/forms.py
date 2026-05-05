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