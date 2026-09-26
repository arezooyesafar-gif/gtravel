from datetime import date

from django.core.management.base import BaseCommand

from tour.dataset import roll_over_expired_tour_dates
from tour.models import Tour


class Command(BaseCommand):
    help = (
        "Roll over expired tour start/end dates to their next available date_plan, "
        "or unpublish the tour if none remain."
    )

    def handle(self, *args, **options):
        expired_tours = Tour.objects.filter(StartDate__lte=date.today(), PubTour=True)
        count = expired_tours.count()
        self.stdout.write(f"Rolling over {count} expired tour(s)...")
        roll_over_expired_tour_dates(expired_tours)
        self.stdout.write(self.style.SUCCESS(f"Done. Processed {count} tour(s)."))
