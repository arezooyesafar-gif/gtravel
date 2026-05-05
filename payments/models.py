from django.db import models


class PaymentRequest(models.Model):
    STATUS_CHOICES = (
        (1, 'ناموفق'),
        (2, 'موفق')
    )
    status = models.IntegerField(default=1, choices=STATUS_CHOICES)
    contract_number = models.CharField(
        max_length=128,
        blank=True,
        null=True,
    )
    full_name = models.CharField(
        max_length=256,
        blank=True,
        null=True,
    )
    phone_number = models.CharField(
        max_length=16,
        blank=True,
        null=True,
    )
    amount = models.DecimalField(max_digits=20, decimal_places=0)
    description = models.TextField(null=True, blank=True)
    terminal_id = models.CharField(
        max_length=32,
        blank=True,
        null=True,
    )
    res_number = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        unique=True
    )
    token = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        unique=True
    )
    rrn = models.CharField(
        max_length=128,
        blank=True,
        null=True,
    )
    ref_number = models.CharField(
        max_length=128,
        blank=True,
        null=True,
    )
    trace_number = models.CharField(
        max_length=128,
        blank=True,
        null=True
    )
    secure_pan = models.CharField(
        max_length=128,
        blank=True,
        null=True,
    )
    hashed_card_number = models.CharField(
        max_length=256,
        blank=True,
        null=True,
    )
    callback_status_code = models.IntegerField(null=True, blank=True)
    verify_result_code = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
