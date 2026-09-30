from captcha.fields import CaptchaField

import blog.models
from .models import *
from django import forms
from hotels.models import hotel_comments

class CreatePostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['Category'].empty_lable = 'دسته بندی مطلب را انتخاب کنید'
        self.fields['Image'].widget = forms.FileInput(attrs={'class': 'input-text hide-field'})
        self.fields['Image'].widget.attrs.update({
            'class': 'hide-field'
        })
        self.fields['Title'].widget.attrs.update({
            'class': 'text-input'
        })
        self.fields['ptitle'].widget.attrs.update({
            'class': 'text-input'
        })
        self.fields['author'].widget.attrs.update({
            'class': 'text-input'
        })
        self.fields['slug'].widget.attrs.update({
            'class': 'text-input'
        })
        self.fields['Category'].widget.attrs.update({
            'class': 'text-input'
        })
        self.fields['meta_robots'].widget.attrs.update({
            'class': 'text-input'
        })
        self.fields['metaKeyword'].widget.attrs.update({
            'class': 'text-input',
            'cols': '50',
            'rows': '3'
        })
        self.fields['metaDescription'].widget.attrs.update({
            'class': 'text-input',
            'cols': '50',
            'rows': '3'
        })

    class Meta:
        model = blogPosts
        fields = '__all__'

class CreatePostCategoryForm(forms.ModelForm):
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
        model = PostCategory
        fields = '__all__'

class comment_form(forms.ModelForm):
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
            }
        )


    class Meta:
        model = comments
        exclude = ['post']

class relatedPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['related_post'].widget.attrs.update({
                'class': 'form-select',
        })

    class Meta:
        model = related_posts
        exclude = ['post']
