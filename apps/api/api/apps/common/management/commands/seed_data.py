import datetime

from django.core.management.base import BaseCommand

from divisions.models import Division
from seasons.models import Season


DIVISIONS = ['Division 1', 'Division 2', 'Division 3', 'Division 4']
SEASONS = list(range(2010, 2031))


class Command(BaseCommand):
    help = 'Seed data for local development purposes.'

    def handle(self, *args, **options):
        print(f'Seeding {len(DIVISIONS)} divisions.')
        for d in DIVISIONS:
            obj, created = Division.objects.get_or_create(name=d)
            print(f'  {obj} {"created" if created else "already exists"}.')

        print(f'Seeding {len(SEASONS)} seasons.')
        for s in SEASONS:
            start = datetime.date(year=s, month=3, day=1)
            obj, created = Season.objects.get_or_create(start=start, end=start + datetime.timedelta(weeks=4 * 8))
            print(f' {obj} {"created" if created else "already exists"}.')
