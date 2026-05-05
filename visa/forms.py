from django import forms
from .models import *


class DateInput(forms.DateInput):
    input_type = 'date'
    is_required = False

class visa_request_form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cz_passport'].required = True
        self.fields['rq_father_brd'] = forms.DateField(widget=DateInput)
        self.fields['rq_mother_brd'] = forms.DateField(widget=DateInput)
        self.fields['passport_issue'] = forms.DateField(widget=DateInput)
        self.fields['passport_expire'] = forms.DateField(widget=DateInput)
        self.fields['data_entry_russia'] = forms.DateField(widget=DateInput)
        self.fields['partner_brd_date'] = forms.DateField(widget=DateInput)
        self.fields['military_start_date'] = forms.DateField(widget=DateInput)
        self.fields['military_end_date'] = forms.DateField(widget=DateInput)
        self.fields['military_start_date'].required = False
        self.fields['military_end_date'].required = False
        self.fields['partner_brd_date'].required = False
        self.fields['person_image'] = forms.ImageField(widget=forms.FileInput())
        self.fields['passport_image'] = forms.ImageField(widget=forms.FileInput())
        self.fields['passport_expire'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['data_entry_russia'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['partner_brd_date'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['relation_phone'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['requester_id_number'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['requester_family'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['requester_name'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['rq_father_name'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['rq_father_family'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['rq_father_brd'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['rq_father_brd_location'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['rq_mother_name'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['rq_mother_family'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['rq_mother_brd'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['rq_mother_brd_location'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['address'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['phone'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['job_title'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['job_address'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['job_phone'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['job_email'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['passport_image'].widget.attrs.update({
            'class': 'form-control hide'
        })
        self.fields['person_image'].widget.attrs.update({
            'class': 'form-control hide'
        })
        self.fields['visa_file'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['old_name'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['name_change_date'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['name_change_reason'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['cz_country'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['cz_passport'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['gc_country'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['gc_start_date'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['gc_end_date'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['gc_id_number'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['travel_history'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['social_media'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['partner_name'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['partner_family'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['partner_brd_date'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['partner_brd_location'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['uni_name'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['uni_address'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['military_start_date'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['military_end_date'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['military_type'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['military_location'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['travel_reason'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['hotel_name'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['passport_issue'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['passport_expire'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['data_entry_russia'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['relation_degree'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['relation_name'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['relation_family'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['relation_sex'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['relation_Address'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['relation_brd_date'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['orogin_name'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['orogin_address'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['orogin_phone'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['orogin_email'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['orogin_city'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['visa_file'].widget.attrs.update({
            'class': 'form-control'
        })

    class Meta:
        model = visa_request_item
        exclude = ['user', 'confirmed', 'req_stat', 'payment_stat', 'trs_number']


class thaiVisaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rqquester_brd'] = forms.DateField(widget=DateInput)
        self.fields['passport_issue'] = forms.DateField(widget=DateInput)
        self.fields['passport_expire'] = forms.DateField(widget=DateInput)
        self.fields['thai_entry'] = forms.DateField(widget=DateInput)
        self.fields['thai_exit'] = forms.DateField(widget=DateInput)
        self.fields['person_image'] = forms.ImageField(widget=forms.FileInput())
        self.fields['passport_image'] = forms.ImageField(widget=forms.FileInput())
        self.fields['person_brd_image'] = forms.ImageField(widget=forms.FileInput())
        self.fields['person_id_image'] = forms.ImageField(widget=forms.FileInput())
        self.fields['person_hotel_image'] = forms.ImageField(widget=forms.FileInput())
        self.fields['person_flight_image'] = forms.ImageField(widget=forms.FileInput())
        self.fields['passport_image'].widget.attrs.update({
            'class': 'form-control hide'
        })
        self.fields['person_image'].widget.attrs.update({
            'class': 'form-control hide'
        })
        self.fields['person_brd_image'].widget.attrs.update({
            'class': 'form-control hide'
        })
        self.fields['person_id_image'].widget.attrs.update({
            'class': 'form-control hide'
        })
        self.fields['person_hotel_image'].widget.attrs.update({
            'class': 'form-control hide'
        })
        self.fields['person_flight_image'].widget.attrs.update({
            'class': 'form-control hide'
        })
        self.fields['visa_file'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['passport_number'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['passport_issue'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['passport_expire'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['rqquester_brd'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['thai_entry'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['thai_exit'].widget.attrs.update({
            'class': 'form-control'
        })

        self.fields['requester_name'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['requester_family'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['requester_Nationality'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['requester_brd_city'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['requester_country'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['requester_city'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['address'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['phone'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['marial_stat'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['job_title'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['job_company'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['income'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['job_owner'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['thai_trip'].widget.attrs.update({
            'class': 'form-control'
        })

        self.fields['thai_applied'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['inviter_name'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['inviter_city'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['inviter_phone'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['inviter_email'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['inviter_address'].widget.attrs.update({
            'class': 'form-control'
        })


    class Meta:
        model = ThaiVisa
        exclude = ['user', 'confirmed', 'req_stat', 'payment_stat', 'trs_number']