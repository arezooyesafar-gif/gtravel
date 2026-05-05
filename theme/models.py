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

    def __str__(self):
        return str(self.hotel_reserve)
