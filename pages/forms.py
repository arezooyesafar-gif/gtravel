from .models import *
from django import forms

class PageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PageForm, self).__init__(*args, **kwargs)
        self.fields['page_image'].widget = forms.FileInput(attrs={'class': 'input-text hide-field'})
        self.fields['title'].widget.attrs.update({
            'class': 'text-input'
        })
        self.fields['short_content'].widget.attrs.update({
            'class': 'text-input'
        })
        self.fields['content'].widget.attrs.update({
            'class': 'text-input'
        })
        self.fields['slug'].widget.attrs.update({
            'class': 'text-input'
        })
        self.fields['meta_keyword'].widget.attrs.update({
            'class': 'text-input'
        })
        self.fields['meta_desc'].widget.attrs.update({
            'class': 'text-input',
            'rows': '5'
        })
    class Meta:
        model = pages
        fields = '__all__'

class FileUploadForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FileUploadForm, self).__init__(*args, **kwargs)
        self.fields['file'].widget.attrs.update({
            'class': 'file_upload'
        })
    class Meta:
        model = UploadedFile
        fields = ['file']