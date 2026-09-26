from django.contrib import admin
from .models import *


class TourAdmin(admin.ModelAdmin):
    list_display = ['Title', 'StartDate', 'EndDate']


class HotelAdmin(admin.ModelAdmin):
    list_display = ['HotelName','HotelRating']


class AirLineAdmin(admin.ModelAdmin):
    list_display = ['AirLineTitle']


class PackageAdmin(admin.ModelAdmin):
    list_display = ['TourName']


class PostsAdmin(admin.ModelAdmin):
    list_display = ['Title']


class TourMenuAdmin(admin.ModelAdmin):
    list_display = ['MenuTitle']


class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ['CatName']

class FooterAdmin(admin.ModelAdmin):
    list_display = ['Address', 'Phone', 'dollar_rate']

admin.site.register(Tour, TourAdmin)
admin.site.register(AirLineData, AirLineAdmin)
admin.site.register(Package, PackageAdmin)
# admin.site.register(Posts, PostsAdmin)
admin.site.register(TourMenu, TourMenuAdmin)
# admin.site.register(PostCategory, PostCategoryAdmin)
