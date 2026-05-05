from django.contrib.sitemaps import Sitemap
from .models import Tour

class TourSitemap(Sitemap):
	def items(self):
		return Tour.objects.all()

