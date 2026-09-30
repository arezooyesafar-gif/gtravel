from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django_resized import ResizedImageField
from django.urls import reverse


ROBOTS_CHOICES = [
    ('INDEX,FOLLOW', 'Index, Follow - (پیش‌فرض) نمایش در نتایج و دنبال کردن لینک‌ها'),
    ('INDEX,NOFOLLOW', 'Index, No Follow - نمایش در نتایج، دنبال نکردن لینک‌ها'),
    ('NOINDEX,FOLLOW', 'No Index, Follow - عدم نمایش در نتایج، دنبال کردن لینک‌ها'),
    ('NOINDEX,NOFOLLOW', 'No Index, No Follow - عدم نمایش در نتایج و دنبال نکردن لینک‌ها'),
]

class PostCategory(models.Model):
    CatName = models.CharField(max_length=500)
    parentCat = models.ForeignKey('self', related_name='Children', on_delete=models.CASCADE, null=True, blank=True)
    slug = models.SlugField()
    page_title = models.CharField(max_length=500, null=True, blank=True)
    meta_desc = models.CharField(max_length=500, null=True, blank=True)
    meta_keyword = models.CharField(max_length=500, null=True, blank=True)
    country = models.ForeignKey('tour.Country', on_delete=models.SET_NULL, null=True, blank=True, related_name='post_categories', verbose_name='کشور')

    def __str__(self):
        full_path = [self.CatName]
        k = self.parentCat
        while k is not None:
            full_path.append(k.CatName)
            k = k.parentCat
        return ' - '.join(full_path[::-1])

class blogPosts(models.Model):
    Title = models.CharField(max_length=500, verbose_name='عنوان مقاله')
    Category = models.ForeignKey(PostCategory, on_delete=models.CASCADE, null=True, blank=True)
    ShortDesc = RichTextField(max_length=6000)
    post_links = RichTextField(max_length=6000, null=True, blank=True)
    Description = RichTextUploadingField(max_length=100000)
    Image = ResizedImageField(force_format='WEBP', quality=75, upload_to='media/post/main-image')
    slug = models.SlugField()
    Publish = models.BooleanField(default=True)
    PubDate = models.DateField(auto_now_add=True, null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, null=True, blank=True) 
    metaKeyword = models.TextField(max_length=300, null=True, blank=True)
    metaDescription = models.TextField(max_length=150, null=True, blank=True)
    viewCount = models.IntegerField(default=0, null=True, blank=True)
    ptitle = models.CharField(max_length=500, null=True, blank=True)
    author = models.CharField(max_length=150, blank=True, default='حدیثه محمدی', verbose_name='نویسنده')
    meta_robots = models.CharField(
        max_length=50,
        choices=ROBOTS_CHOICES,
        default='INDEX,FOLLOW',
        verbose_name='وضعیت نمایش در موتورهای جستجو (SEO)',
        help_text='تنظیم کنید که این صفحه در گوگل دیده شود یا خیر'
    )

    def __str__(self):
        return self.Title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'id':self.id,'slug': self.slug})

    class Meta:
        verbose_name = ' مطالب '
        verbose_name_plural = ' مطالب '

class comments(models.Model):
    post = models.ForeignKey(blogPosts, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=300)
    email = models.EmailField()
    desc = models.TextField(max_length=5000)
    create_date = models.DateField(auto_now_add=True, null=True, blank=True)
    publish = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name

class reply_comments(models.Model):
    comment = models.ForeignKey(comments, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=300)
    email = models.EmailField()
    desc = models.TextField(max_length=5000)
    create_date = models.DateField(auto_now_add=True, null=True, blank=True)
    publish = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name

class related_posts(models.Model):
    post = models.ForeignKey(blogPosts, on_delete=models.CASCADE)
    related_post = models.ForeignKey(blogPosts, on_delete=models.CASCADE, related_name='related_article')