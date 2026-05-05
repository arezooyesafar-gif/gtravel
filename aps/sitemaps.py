from django.contrib.sitemaps import Sitemap
from tour.models import *
from blog.models import *
from hotels.models import *


class blogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = 'https'

    def items(self):
        return blogPosts.objects.filter(Publish=True)

    def lastmod(self, obj):
        return obj.PubDate

    def location(self, obj):
        return '/blog/%s/%s' % (obj.id, obj.slug)

class tourContrySitemap(Sitemap):
    changefreq = "daily"
    priority = 1.0
    protocol = 'https'

    def items(self):
        return Country.objects.filter(tocountry__PubTour=True, tocountry__isnull=False).distinct()

    # def lastmod(self, obj):
    #     return obj.updateDate

    def location(self, obj):
        return '/%s/%s/all-tour' % (obj.slug, obj.id)

class tourCitySitemap(Sitemap):
    changefreq = "daily"
    priority = 1.0
    protocol = 'https'

    def items(self):
        return City.objects.filter(tour_city__PubTour=True, tour_city__isnull=False).distinct()

    # def lastmod(self, obj):
    #     return obj.updateDate

    def location(self, obj):
        return '/%s/%s/city-tours' % (obj.slug, obj.id)

class tourSitemap(Sitemap):
    changefreq = "daily"
    priority = 1.0
    protocol = 'https'

    def items(self):
        return Tour.objects.filter(PubTour=True)

    def lastmod(self, obj):
        return obj.updateDate

    def location(self, obj):
        return '/tour/%s/%s' % (obj.id, obj.Slug)

class hotelSitemap(Sitemap):
    changefreq = "daily"
    priority = 1.0
    protocol = 'https'

    def items(self):
        return Hotel_Data.objects.all()

    def location(self, obj):
        return '/hotels/%s/%s' % (obj.id, obj.Slug)

class hotelCountrySitemap(Sitemap):
    changefreq = "daily"
    priority = 1.0
    protocol = 'https'

    def items(self):
        return Country.objects.filter(hotel_country__isnull=False).distinct()

    def location(self, obj):
        return '/all-country-hotel/%s/%s' % (obj.id, obj.slug)

class hotelCitySitemap(Sitemap):
    changefreq = "daily"
    priority = 1.0
    protocol = 'https'

    def items(self):
        return City.objects.filter(hotel_city__isnull=False).distinct()

    def location(self, obj):
        return '/all-hotel/%s/%s' % (obj.id, obj.slug)

class StaticSitemap(Sitemap):
    changefreq = "monthly"
    priority = 1.0
    protocol = 'https'

    def items(self):
        return ['index-page', 'blog', "all-hotel",
            "all-tour", "norooz_tours", "installment_tours",
            "about-us", "contact-us",]

    def location(self, item):
        return reverse(item)