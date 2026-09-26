from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

class index_page(models.Model):
    internal_ticket = models.BooleanField(default=True,null=True, blank=True)
    external_ticket = models.BooleanField(default=True,null=True, blank=True)
    hotel_reserve = models.BooleanField(default=True,null=True, blank=True)
    st_title = models.CharField(max_length=300,null=True, blank=True)
    about_title =models.CharField(max_length=300,null=True, blank=True)
    about_text = RichTextUploadingField(max_length=5000, null=True, blank=True)
    about_logo = models.ImageField(upload_to='media/index_page',null=True, blank=True)
    about_address = models.CharField(max_length=300,null=True, blank=True)
    about_phone = models.CharField(max_length=300,null=True, blank=True)
    blog_title = models.CharField(max_length=300,null=True, blank=True)
    faq_title = models.CharField(max_length=300,null=True, blank=True)
    box_1_title = models.CharField(max_length=100,null=True, blank=True)
    box_2_title = models.CharField(max_length=100,null=True, blank=True)
    box_3_title = models.CharField(max_length=100,null=True, blank=True)
    box_1_desc = models.CharField(max_length=100,null=True, blank=True)
    box_2_desc = models.CharField(max_length=100,null=True, blank=True)
    box_3_desc = models.CharField(max_length=100,null=True, blank=True)
    footer_phone = models.CharField(max_length=100,null=True, blank=True)
    footer_address = models.CharField(max_length=300,null=True, blank=True)
    google_review_url = models.URLField(
        max_length=500, null=True, blank=True,
        verbose_name='لینک ثبت نظر در گوگل',
        help_text='از Google Business Profile بخش Ask for reviews کپی کنید'
    )
    google_place_id = models.CharField(
        max_length=200, null=True, blank=True,
        verbose_name='شناسهٔ مکان در گوگل (Place ID)',
        help_text='از صفحهٔ Place ID Finder گوگل کپی کنید')
    google_places_key = models.CharField(
        max_length=200, null=True, blank=True,
        verbose_name='کلید Places API',
        help_text='در Google Cloud باید Places API (New) فعال باشد')
    google_api_proxy = models.CharField(
        max_length=200, null=True, blank=True,
        verbose_name='پراکسی درخواست به گوگل (اختیاری)',
        help_text='مثل http://127.0.0.1:10809 وقتی سرور مستقیم به گوگل وصل نمی‌شود')

    def __str__(self):
        return str(self.hotel_reserve)
