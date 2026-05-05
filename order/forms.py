from django import forms
from jalali_date.widgets import AdminJalaliDateWidget


class order_search_form(forms.Form):
    submit_date = forms.DateField(widget=AdminJalaliDateWidget(), required=False)
    paid_date = forms.DateField(widget=AdminJalaliDateWidget(), required=False)

    submit_date.widget.attrs.update({
        'placeholder': 'تاریخ ثبت',
        'autocomplete': 'off',
    })
    paid_date.widget.attrs.update({
        'placeholder': 'تاریخ پرداخت',
        'autocomplete': 'off',
    })
