from django.urls import path
from .views import *

urlpatterns = [
    path('ajax_file_list', ajax_file_list, name='ajax_file_list'),
    path('ajax_ads_files', ajax_ads_files, name='ajax_ads_files'),
    path('create_page', create_page, name='create_page'),
    path('page_update/<int:id>', page_update, name='page_update'),
    path('page_delete/<int:id>', page_delete, name='page_delete'),
    path('page_list', page_list, name='page_list'),
    path('file_list', file_list, name='file_list'),
    path('ads_file_list', ads_file_list, name='ads_file_list'),
    path('upload_file', upload_file, name='upload_file'),
    path('ads_upload_file', ads_upload_file, name='ads_upload_file'),
]