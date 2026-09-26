from django.core.management.base import BaseCommand

from hotels.models import Hotel_Data
from tour.models import City, Country
from tour.templatetags.responsive_img import build_srcset


class Command(BaseCommand):
    help = "Pre-generate WEBP variants used by the hotel list pages"

    def add_arguments(self, parser):
        parser.add_argument("--country", type=int, default=None)
        parser.add_argument("--limit", type=int, default=None)

    def handle(self, *args, **options):
        hotels = Hotel_Data.objects.exclude(HotelImage="").order_by("-id")
        cities = City.objects.exclude(cityImg="").filter(hotel_city__isnull=False).distinct()
        countries = Country.objects.exclude(country_iamge="")
        if options.get("country"):
            hotels = hotels.filter(Hcountry=options["country"])
            cities = cities.filter(hotel_city__Hcountry=options["country"])
            countries = countries.filter(id=options["country"])
        if options.get("limit"):
            hotels = hotels[:options["limit"]]
        jobs = [(countries, "country_iamge", (480, 768)), (cities, "cityImg", (480, 768)), (hotels, "HotelImage", (480, 640))]
        done = 0
        for queryset, field, widths in jobs:
            for obj in queryset.only("id", field):
                try:
                    build_srcset(getattr(obj, field), widths)
                    done += 1
                except Exception as exc:
                    self.stderr.write("%s #%s failed: %s" % (field, obj.pk, exc))
        self.stdout.write(self.style.SUCCESS("Done. %d image(s) processed." % done))
