from .models import *

def get_colm_two_pages():
    return pages.objects.filter(footer_2=True)

def get_colm_tree_pages():
    return pages.objects.filter(footer_3=True)