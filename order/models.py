from django.contrib.auth.models import User
from django.db import models
from tour.models import *

class discount(models.Model):
    code = models.CharField(max_length=10)
    price = models.IntegerField(default=0)

class order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=10, unique=True)
    order_date = models.DateTimeField(auto_now_add=True)
    order_total = models.IntegerField(default=0,null=True, blank=True)
    paid_amount = models.IntegerField(default=0, null=True, blank=True)
    dicount_copon = models.ForeignKey(discount, on_delete=models.CASCADE, null=True, blank=True)
    discount_amount = models.IntegerField(default=0, null=True, blank=True)
    paid = models.BooleanField(default=False)
    paid_date = models.DateTimeField(auto_now_add=True)
    order_close = models.BooleanField(default=False)

    def debit(self):
        return self.order_total - self.paid_amount

class orderItem(models.Model):
    order = models.ForeignKey(order, on_delete=models.CASCADE)
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    adults = models.IntegerField(default=2)
    adults_price = models.IntegerField(default=0)
    baby_with_bed = models.IntegerField(default=0)
    baby_with_bed_price = models.IntegerField(default=0)
    baby_with_out_bed = models.IntegerField(default=0)
    baby_with_out_bed_price = models.IntegerField(default=0)
    infont = models.IntegerField(default=0)
    infont_price = models.IntegerField(default=0)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    total_item_price = models.IntegerField(default=0)
    item_add_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

class orderTransaction(models.Model):
    order = models.ForeignKey(order, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField()
    payment_stat = models.BooleanField(default=False)
    payment_refId = models.CharField(max_length=10, null=True, blank=True)