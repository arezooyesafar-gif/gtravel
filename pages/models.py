from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

class pages(models.Model):
    title = models.CharField(max_length=300)
    page_image = models.ImageField(upload_to='media/pages', blank=True)
    short_content = RichTextUploadingField(null=True, blank=True, max_length=2000)
    content = RichTextUploadingField(null=True, blank=True, max_length=4000)
    slug = models.SlugField(unique=True)
    reseller = models.BooleanField(default=False)
    footer_1 = models.BooleanField(default=False)
    footer_2 = models.BooleanField(default=False)
    footer_3 = models.BooleanField(default=False)
    publish = models.BooleanField(default=False)
    meta_desc = models.TextField(max_length=300, null=True, blank=True)
    meta_keyword = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.title

class UploadedFile(models.Model):
    file = models.FileField(upload_to='ads/')

