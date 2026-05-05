from .models import *

def get_all_blog_posts():
    return blogPosts.objects.all().order_by('-id')

def get_all_blog_cats():
    return PostCategory.objects.all().order_by('-id')