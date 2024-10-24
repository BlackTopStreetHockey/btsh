import datetime

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from divisions.models import Division
from seasons.models import Season
from teams.models import Team


DIVISIONS = ['Division 1', 'Division 2', 'Division 3', 'Division 4']
SEASONS = list(range(2010, 2031))
TEAMS = [
    'Lbs',
    'Gouging Anklebiters',
    'Mega Touch',
    'Renaissance',
    'Sky Fighters',
    'Corlears Hookers',
    'Vertz',
    'Fuzz',
    'Filthier',
    'Poutine Machine',
    'Instant Karma',
    'Cobra Kai',
    'Denim Demons',
    'Fresh Kills',
    'Butchers',
    'Dark Rainbows',
    'Gremlins',
    'Riots',
    'Moby Dekes',
    'What the Puck',
]


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

        print(f'Seeding {len(TEAMS)} teams.')
        for t in TEAMS:
            filename = f'{slugify(t).replace("-", "_")}.jpg'
            logo_path = settings.FIXTURES_DIR / f'team_logos/{filename}'
            with open(logo_path, 'rb') as f:
                logo = File(f, name=filename)

                obj, created = Team.objects.get_or_create(
                    name=t,
                    defaults={
                        'logo': logo,
                        'jersey_colors': None,
                    }
                )
                print(f' {obj} {"created" if created else "already exists"}.')
