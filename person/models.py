from django.contrib.auth.models import User
from django.db import models

class person_profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=20)
    provinace = models.CharField(max_length=300, null=True, blank=True)
    city = models.CharField(max_length=300, null=True, blank=True)
    adress = models.CharField(max_length=500, null=True, blank=True)
    otp_code = models.CharField(max_length=20)

class profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    otp_code = models.CharField(max_length=10)
    agancy_name = models.CharField(max_length=200)
