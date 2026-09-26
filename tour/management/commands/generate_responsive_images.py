from django.core.management.base import BaseCommand

from tour.models import Tour, TripPlan, tour_images, Country, City
from tour.templatetags.responsive_img import build_srcset
from hotels.models import Hotel_Data, hotel_images


class Command(BaseCommand):
    help = "Pre-generate cached srcset (WEBP) variants for tour-detail page images"

    def add_arguments(self, parser):
        parser.add_argument(
            "--limit",
            type=int,
            default=None,
            help="فقط N رکورد اول هر مدل را پردازش کن (برای تست)",
        )

    def handle(self, *args, **options):
        limit = options.get("limit")
        jobs = [
            ("Tour.tour_main", Tour.objects.exclude(tour_main=""), "tour_main"),
            ("Tour.TourImage", Tour.objects.exclude(TourImage=""), "TourImage"),
            ("tour_images.image", tour_images.objects.exclude(image=""), "image"),
            ("TripPlan.plan_image", TripPlan.objects.exclude(plan_image=""), "plan_image"),
            ("Hotel_Data.HotelImage", Hotel_Data.objects.exclude(HotelImage=""), "HotelImage"),
            ("hotel_images.image", hotel_images.objects.exclude(image=""), "image"),
            ("Country.country_iamge", Country.objects.exclude(country_iamge=""), "country_iamge"),
            ("City.cityImg", City.objects.exclude(cityImg=""), "cityImg"),
        ]

        total_ok = 0
        total_fail = 0
        for label, queryset, field_name in jobs:
            qs = queryset.only("id", field_name)
            if limit:
                qs = qs[:limit]
            count = qs.count() if not limit else len(qs)
            self.stdout.write("%s: %d record(s)" % (label, count))
            for obj in qs:
                field_file = getattr(obj, field_name)
                try:
                    entries = build_srcset(field_file)
                    if entries:
                        total_ok += 1
                    else:
                        total_fail += 1
                except Exception as exc:  # pragma: no cover - defensive, never abort the batch
                    total_fail += 1
                    self.stderr.write("  failed on %s #%s: %s" % (label, obj.pk, exc))

        self.stdout.write(self.style.SUCCESS(
            "Done. %d image(s) processed, %d skipped/failed." % (total_ok, total_fail)
        ))
