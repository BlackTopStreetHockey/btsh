import datetime

from django.core.management import BaseCommand

from ...utils import calculate_team_season_registration_stats


class Command(BaseCommand):
    help = 'Calculate team season registration stats'

    def handle(self, *args, **options):
        start = datetime.datetime.now()
        calculate_team_season_registration_stats()
        print(f'\nTook: {datetime.datetime.now() - start}')
