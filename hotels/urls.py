from django.urls import path, include
from .views import *

urlpatterns = [
    path('ajax_hotel_list/', ajax_hotel_list, name='ajax_hotel_list'),
    path('hotel_cities_ajax/', ajax_hotel_cities, name='hotel_cities_ajax'),
    path('create_hotel', create_hotel, name='create_hotel'),
    path('update_hotel/<int:id>', update_hotel, name='update_hotel'),
    path('delete_hotel/<int:id>', delete_hotel, name='delete_hotel'),
    path('hotel_list', hotel_list, name='hotel_list'),
    path('create_hotel_menu', CreateHotelMenu, name='create-hotel-menu'),
    path('update_hotel_menu/<int:id>', UpdateHotelMenu, name='update-hotel-menu'),
    path('delete_hotel_menu/<int:id>', DeleteHotelMenu, name='delete-hotel-menu'),
    path('remove_gallery_item/<int:id>', remove_gallery_item, name='remove_gallery_item'),
    path('remove_hotel_image/<int:id>', remove_hotel_image, name='remove_hotel_image'),
    path('hotel_comment_list/', comment_list, name='comment_list'),
    path('comment_update/<int:id>', comment_update, name='comment_update'),
    path('comment_delete/<int:id>', comment_delete, name='comment_delete'),
]