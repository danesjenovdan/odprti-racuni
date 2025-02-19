from datetime import date

from django.core.management.base import BaseCommand

from nvo import models


class Command(BaseCommand):
    help = "Create financial year if it does not exist"

    def handle(self, *args, **options):
        current_year = date.today().year
        last_year = current_year - 1
        models.FinancialYear.objects.get_or_create(
            name=last_year,
            start_date=date(day=1, month=1, year=last_year),
            end_date=date(day=31, month=12, year=last_year),
        )
