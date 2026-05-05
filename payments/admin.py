from django.contrib import admin
from payments.models import *


@admin.register(PaymentRequest)
class PaymentRequestAdmin(admin.ModelAdmin):
    list_display = (
        'contract_number',
        'full_name',
        'phone_number',
        'camma_amount',
        'description',
        'status',
        'terminal_id',
        'res_number',
        'rrn',
        'ref_number',
        'trace_number',
        'secure_pan',
        'hashed_card_number',
        'created_at'
    )
    search_fields = (
        'contract_number',
        'full_name',
        'phone_number',
        'res_number',
        'rrn',
        'ref_number',
        'status'
    )
    list_filter = ['status']

    def camma_amount(self, obj):
        return f'{int(obj.amount):,d} ریال'
