from django.contrib.auth.models import User
from django.db import models
from order.models import *

class wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.IntegerField(default=0, null=True, blank=True)

class walletTransaction(models.Model):
    wallet = models.ForeignKey(wallet, on_delete=models.CASCADE)
    amount = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField()
    deposit = models.BooleanField(default=False)
    withdrawal = models.BooleanField(default=False)
    order = models.ForeignKey(order, on_delete=models.CASCADE, null=True, blank=True)
    deposit_form_order_cancel = models.BooleanField(default=False)
    withdraw_form_order_payment = models.BooleanField(default=False)
    payment_stat = models.BooleanField(default=False)
    payment_refId = models.CharField(max_length=10, null=True, blank=True)