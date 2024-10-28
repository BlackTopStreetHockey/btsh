import datetime
import random

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify

from divisions.models import Division
from games.models import Game, GameDay
from seasons.models import Season
from teams.models import Team
from users.models import User


CURRENT_YEAR = timezone.now().date().year
YEAR_DIFF = 2

DIVISIONS = ['Division 1', 'Division 2', 'Division 3', 'Division 4']
SEASONS = list(range(CURRENT_YEAR - YEAR_DIFF, CURRENT_YEAR + YEAR_DIFF))
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


def get_sundays_for_date_range(start_date, end_date):
    start_date += datetime.timedelta(days=(6 - start_date.weekday()))
    sundays = []

    while start_date <= end_date:
        sundays.append(start_date)
        start_date += datetime.timedelta(days=7)
    return sundays


def get_or_create(cls, get_kwargs, create_kwargs):
    try:
        obj = cls.objects.get(**get_kwargs)
        created = False
    except cls.DoesNotExist:
        obj = cls(**create_kwargs)
        obj.full_clean()
        obj.save()
        created = True
    print(f'[{cls._meta.verbose_name}] {obj} {"created" if created else "already exists"}.')
    return obj, created


def print_separator():
    print()
    print('*' * 50)
    print()


class Command(BaseCommand):
    help = 'Seed data for local development purposes.'

    def handle(self, *args, **options):
        users = User.objects.filter(is_superuser=True)
        if not users.exists():
            print('Please create a superuser to continue.')
            return

        created_by = users.first()
        divisions = []
        seasons = []
        teams = []
        games = []

        print(f'Seeding {len(DIVISIONS)} divisions.')
        for d in DIVISIONS:
            division, _ = get_or_create(
                Division, get_kwargs={'name': d}, create_kwargs={'name': d, 'created_by': created_by}
            )
            divisions.append(division)

        print_separator()

        print(f'Seeding {len(SEASONS)} seasons.')
        for s in SEASONS:
            start = datetime.date(year=s, month=3, day=1)
            end = start + datetime.timedelta(weeks=4 * 8)
            season, _ = get_or_create(
                Season,
                get_kwargs={'start': start, 'end': end},
                create_kwargs={'start': start, 'end': end, 'created_by': created_by}
            )
            seasons.append(season)

        print_separator()

        print(f'Seeding {len(TEAMS)} teams.')
        for t in TEAMS:
            filename = f'{slugify(t).replace("-", "_")}.jpg'
            logo_path = settings.FIXTURES_DIR / f'team_logos/{filename}'
            with open(logo_path, 'rb') as f:
                logo = File(f, name=filename)
                team, _ = get_or_create(
                    Team,
                    get_kwargs={'name': t},
                    create_kwargs={'name': t, 'logo': logo, 'jersey_colors': None, 'created_by': created_by}
                )
                teams.append(team)

        print_separator()

        for season in seasons:
            sundays = get_sundays_for_date_range(season.start, season.end)
            num_games_per_day = 10

            print(f'Seeding game days and games for {season}.')
            for sunday in sundays:
                matchups = []
                for i in range(num_games_per_day):
                    home = teams[i]
                    away = teams[-i - 1]
                    matchups.append((home, away))
                teams.insert(1, teams.pop())

                opening_team, closing_team = random.sample(teams, 2)
                game_day, _ = get_or_create(
                    GameDay,
                    get_kwargs={'day': sunday},
                    create_kwargs={
                        'day': sunday,
                        'season': season,
                        'opening_team': opening_team,
                        'closing_team': closing_team,
                        'created_by': created_by,
                    }
                )

                print()

                game_number = 0
                start_hour = 12
                offsets = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7]
                for home_team, away_team in matchups:
                    start_offset = offsets[game_number]
                    start = datetime.time(hour=start_hour + start_offset, minute=0)
                    court = Game.EAST if game_number % 2 == 0 else Game.WEST
                    game, _ = get_or_create(
                        Game,
                        get_kwargs={
                            'game_day': game_day,
                            'start': start,
                            'home_team': home_team,
                            'away_team': away_team,
                        },
                        create_kwargs={
                            'game_day': game_day,
                            'start': start,
                            'home_team': home_team,
                            'away_team': away_team,
                            'court': court,
                            'created_by': created_by,
                        },
                    )
                    games.append(game)
                    game_number += 1

                print_separator()

        print(f'Seeded {len(games)} games.')
