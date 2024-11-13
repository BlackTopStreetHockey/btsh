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
SHORT_NAMES = [
    'LBS',
    'GANK',
    'MEGA',
    'RENS',
    'SKYF',
    'HOOK',
    'VERT',
    'FUZZ',
    'FLTH',
    'POUT',
    'IK',
    'CK',
    'DEMS',
    'FK',
    'BTCH',
    'DRKR',
    'GREM',
    'RIOT',
    'MOBY',
    'WTP',
]
JERSEY_COLORS = ['Red', 'Orange', 'Yellow', 'Green', 'Blue', 'White', 'Black', 'Purple', 'Gray']
ESTABLISHMENT_YEARS = {
    'Lbs': 2010,
    'Gouging Anklebiters': 2012,
    'Mega Touch': 2015,
    'Renaissance': 2013,
    'Sky Fighters': 2011,
    'Corlears Hookers': 2014,
    'Vertz': 2016,
    'Fuzz': 2012,
    'Filthier': 2015,
    'Poutine Machine': 2013,
    'Instant Karma': 2014,
    'Cobra Kai': 2017,
    'Denim Demons': 2016,
    'Fresh Kills': 2011,
    'Butchers': 2015,
    'Dark Rainbows': 2018,
    'Gremlins': 2014,
    'Riots': 2013,
    'Moby Dekes': 2016,
    'What the Puck': 2001,
}
TEAM_DESCRIPTIONS = {
    'Lbs': 'League champions in 2012, 2015, and 2018. Known for their aggressive defense.',
    'Gouging Anklebiters': 'Champions in 2016. Renowned for their speed and agility.',
    'Mega Touch': 'Won championships in 2017, 2019. Famous for their precise passing game.',
    'Renaissance': 'League champions in 2013, 2014. Traditional powerhouse team.',
    'Sky Fighters': 'Champions in 2011, 2020. Aerial specialists.',
    'Corlears Hookers': 'Won the title in 2015. Known for their unique playing style.',
    'Vertz': 'Championship victories in 2018, 2021. Rising stars of the league.',
    'Fuzz': 'League champions in 2014, 2016, 2019. Defensive specialists.',
    'Filthier': 'Won it all in 2017. Famous for their physical play.',
    'Poutine Machine': 'Champions in 2015, 2020. Canadian-style hockey at its finest.',
    'Instant Karma': 'League winners in 2016, 2018. Known for their comebacks.',
    'Cobra Kai': 'Champions in 2019. No mercy on the ice.',
    'Denim Demons': 'Won championships in 2017, 2021. Style icons of the league.',
    'Fresh Kills': 'League champions in 2012, 2013. Original dynasty team.',
    'Butchers': 'Champions in 2016, 2020. Powerful offensive team.',
    'Dark Rainbows': 'Won their first title in 2021. Up-and-coming contenders.',
    'Gremlins': 'League champions in 2015, 2017. Night game specialists.',
    'Riots': 'Won it all in 2014, 2018. High-energy playing style.',
    'Moby Dekes': 'Champions in 2019, 2021. Masters of deception on ice.',
    'What the Puck': 'League champions in 2011, 2013, 2016. Original franchise with rich history.',
}
TEAM_INSTAGRAM_URLS = {
    'Lbs': 'https://instagram.com/lbs_hockey',
    'Gouging Anklebiters': 'https://instagram.com/anklebiters_hockey',
    'Mega Touch': 'https://instagram.com/mega_touch_hockey',
    'Renaissance': 'https://instagram.com/renaissance_hockey',
    'Sky Fighters': 'https://instagram.com/sky_fighters_hockey',
    'Corlears Hookers': 'https://instagram.com/corlears_hockey',
    'Vertz': 'https://instagram.com/vertz_hockey',
    'Fuzz': 'https://instagram.com/fuzz_hockey',
    'Filthier': 'https://instagram.com/filthier_hockey',
    'Poutine Machine': 'https://instagram.com/poutine_machine_hockey',
    'Instant Karma': 'https://instagram.com/instant_karma_hockey',
    'Cobra Kai': 'https://instagram.com/cobra_kai_hockey',
    'Denim Demons': 'https://instagram.com/denim_demons_hockey',
    'Fresh Kills': 'https://instagram.com/fresh_kills_hockey',
    'Butchers': 'https://instagram.com/butchers_hockey',
    'Dark Rainbows': 'https://instagram.com/dark_rainbows_hockey',
    'Gremlins': 'https://instagram.com/gremlins_hockey',
    'Riots': 'https://instagram.com/riots_hockey',
    'Moby Dekes': 'https://instagram.com/moby_dekes_hockey',
    'What the Puck': 'https://instagram.com/what_the_puck_hockey',
}


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
        for idx, team_name in enumerate(TEAMS):
            filename = f'{slugify(team_name).replace("-", "_")}.jpg'
            logo_path = settings.FIXTURES_DIR / f'team_logos/{filename}'
            with open(logo_path, 'rb') as f:
                logo = File(f, name=filename)
                jersey_colors = random.sample(JERSEY_COLORS, random.randint(1, 2))
                team, _ = get_or_create(
                    Team,
                    get_kwargs={'name': team_name},
                    create_kwargs={
                        'name': team_name,
                        'logo': logo,
                        'jersey_colors': jersey_colors,
                        'created_by': created_by,
                        'short_name': SHORT_NAMES[idx],
                        'established': ESTABLISHMENT_YEARS.get(team_name),
                        'description': TEAM_DESCRIPTIONS.get(team_name),
                        'instagram_url': TEAM_INSTAGRAM_URLS.get(team_name)
                    }
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
