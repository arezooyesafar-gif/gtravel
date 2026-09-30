import re
from datetime import date, datetime

from django.contrib.sitemaps import Sitemap
from django.contrib.sitemaps.views import sitemap
from django.http import Http404
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.encoding import iri_to_uri

from blog.models import PostCategory, blogPosts
from hotels.models import Hotel_Data
from pages.models import pages
from tour.models import City, Country, MemoryCategory, PMemories, Tour

DOMAIN = 'arezoosafar.com'
JUNK_SLUG = re.compile(r'_copy|(^|[-_])test($|[-_\d])', re.I)


def indexable(robots):
    return not (robots or '').strip().upper().startswith('NOINDEX')


def good_slug(slug):
    return bool(slug) and '/' not in slug and not JUNK_SLUG.search(slug)


def day(value):
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    return None


def newest(values):
    days = [d for d in (day(v) for v in values) if d]
    return max(days) if days else None


def public_tours():
    return [t for t in Tour.objects.filter(PubTour=True).only('id', 'Slug', 'meta_robots', 'updateDate', 'norooz', 'Installment', 'Tcountry', 'Tcity') if indexable(t.meta_robots) and good_slug(t.Slug)]


def public_posts():
    return [p for p in blogPosts.objects.filter(Publish=True).only('id', 'slug', 'meta_robots', 'PubDate', 'modified_date', 'Category') if indexable(p.meta_robots) and good_slug(p.slug)]


def post_day(post):
    return day(post.modified_date) or day(post.PubDate)


class EntrySitemap(Sitemap):
    protocol = 'https'

    def entries(self):
        return []

    def items(self):
        return list(self.entries())

    def location(self, item):
        return iri_to_uri(item[0])

    def lastmod(self, item):
        return item[1]

    def get_domain(self, site=None):
        return DOMAIN


class PagesSitemap(EntrySitemap):
    def entries(self):
        tours = public_tours()
        posts = public_posts()
        memos = list(PMemories.objects.filter(publish=True).only('id', 'created_date'))
        yield reverse('index-page'), newest(t.updateDate for t in tours)
        yield reverse('all-tour'), newest(t.updateDate for t in tours)
        yield reverse('norooz_tours'), newest(t.updateDate for t in tours if t.norooz)
        yield reverse('installment_tours'), newest(t.updateDate for t in tours if t.Installment)
        yield reverse('all-hotel'), None
        yield reverse('blog'), newest(post_day(p) for p in posts)
        yield reverse('memories'), newest(m.created_date for m in memos)
        yield reverse('russia_visa'), None
        yield reverse('about-us'), None
        yield reverse('contact-us'), None
        for page in pages.objects.filter(publish=True).only('id', 'slug').order_by('id'):
            if good_slug(page.slug):
                yield '/pages/%s' % page.slug, None


class ToursSitemap(EntrySitemap):
    def entries(self):
        for tour in sorted(public_tours(), key=lambda t: t.id):
            yield '/tour/%s/%s' % (tour.id, tour.Slug), day(tour.updateDate)


class CountriesSitemap(EntrySitemap):
    def entries(self):
        tours = public_tours()
        by_country = {}
        by_city = {}
        for tour in tours:
            if tour.Tcountry_id:
                by_country.setdefault(tour.Tcountry_id, []).append(tour.updateDate)
            if tour.Tcity_id:
                by_city.setdefault(tour.Tcity_id, []).append(tour.updateDate)
        for country in Country.objects.filter(id__in=by_country).only('id', 'slug', 'tour_meta_robots').order_by('id'):
            if country.slug and indexable(country.tour_meta_robots):
                yield '/%s/%s/all-tour' % (country.slug, country.id), newest(by_country[country.id])
        for city in City.objects.filter(id__in=by_city).only('id', 'slug', 'tour_meta_robots').order_by('id'):
            if city.slug and indexable(city.tour_meta_robots):
                yield '/%s/%s/city-tours' % (city.slug, city.id), newest(by_city[city.id])


class BlogSitemap(EntrySitemap):
    def entries(self):
        for post in sorted(public_posts(), key=lambda p: p.id):
            yield '/blog/%s/%s' % (post.id, post.slug), post_day(post)


class BlogCategoriesSitemap(EntrySitemap):
    def entries(self):
        latest = {}
        for post in public_posts():
            if post.Category_id:
                latest.setdefault(post.Category_id, []).append(post_day(post))
        categories = list(PostCategory.objects.only('id', 'slug', 'parentCat').order_by('id'))
        for category in categories:
            dates = list(latest.get(category.id, []))
            for child in categories:
                if child.parentCat_id == category.id:
                    dates += latest.get(child.id, [])
            if dates and category.slug:
                yield '/blog/%s/%s' % (category.slug, category.id), newest(dates)


class HotelsSitemap(EntrySitemap):
    def entries(self):
        hotels = [h for h in Hotel_Data.objects.only('id', 'Slug', 'meta_robots', 'Hcountry', 'Hcity').order_by('id') if indexable(h.meta_robots) and good_slug(h.Slug)]
        for hotel in hotels:
            yield '/hotels/%s/%s' % (hotel.id, hotel.Slug), None
        country_ids = {h.Hcountry_id for h in hotels}
        city_ids = {h.Hcity_id for h in hotels}
        for country in Country.objects.filter(id__in=country_ids).only('id', 'slug', 'hotel_meta_robots').order_by('id'):
            if country.slug and indexable(country.hotel_meta_robots):
                yield '/all-country-hotel/%s/%s' % (country.id, country.slug), None
        for city in City.objects.filter(id__in=city_ids).only('id', 'slug', 'hotel_meta_robots').order_by('id'):
            if city.slug and indexable(city.hotel_meta_robots):
                yield '/all-hotel/%s/%s' % (city.id, city.slug), None


class ItinerariesSitemap(EntrySitemap):
    def entries(self):
        memos = [m for m in PMemories.objects.filter(publish=True).only('id', 'meta_robots', 'category', 'created_date').order_by('id') if indexable(m.meta_robots)]
        latest = {}
        for memo in memos:
            if memo.category_id:
                latest.setdefault(memo.category_id, []).append(memo.created_date)
        for category in MemoryCategory.objects.filter(id__in=latest).only('id', 'slug').order_by('id'):
            if category.slug:
                yield '/itineraries/%s' % category.slug, newest(latest[category.id])
        for memo in memos:
            yield '/read-jounery/%s' % memo.id, day(memo.created_date)


SITEMAPS = {
    'pages': PagesSitemap,
    'tours': ToursSitemap,
    'countries': CountriesSitemap,
    'blog': BlogSitemap,
    'blog-categories': BlogCategoriesSitemap,
    'hotels': HotelsSitemap,
    'itineraries': ItinerariesSitemap,
}


def sitemap_index(request):
    items = []
    for name, sitemap_class in SITEMAPS.items():
        items.append({
            'location': 'https://%s/sitemap-%s.xml' % (DOMAIN, name),
            'last_mod': sitemap_class().get_latest_lastmod(),
        })
    return TemplateResponse(request, 'sitemap_index.xml', {'sitemaps': items}, content_type='application/xml')


def sitemap_section(request, section):
    if section not in SITEMAPS:
        raise Http404
    return sitemap(request, sitemaps=SITEMAPS, section=section)
