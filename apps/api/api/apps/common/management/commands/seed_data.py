import datetime
import random

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify
from mimesis import Person

from divisions.models import Division
from games.models import Game, GameDay
from seasons.models import Season
from teams.models import Team, TeamSeasonRegistration
from users.models import User, UserSeasonRegistration
from .utils import get_default_created_by, get_or_create, print_separator


person = Person()

CURRENT_YEAR = timezone.now().date().year
YEAR_DIFF = 2
USERS_PER_TEAM = 20
TEAMS_PER_DIVISION = 5

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
SHORT_NAMES = {
    'Butchers': 'BTCH',
    'Cobra Kai': 'CK',
    'Corlears Hookers': 'HOOK',
    'Dark Rainbows': 'DRKR',
    'Denim Demons': 'DEMS',
    'Filthier': 'FLTH',
    'Fresh Kills': 'FK',
    'Fuzz': 'FUZZ',
    'Gouging Anklebiters': 'GANK',
    'Gremlins': 'GREM',
    'Instant Karma': 'IK',
    'Lbs': 'LBS',
    'Mega Touch': 'MEGA',
    'Moby Dekes': 'MOBY',
    'Poutine Machine': 'POUT',
    'Renaissance': 'RENS',
    'Riots': 'RIOT',
    'Sky Fighters': 'SKYF',
    'Vertz': 'VERT',
    'What the Puck': 'WTP',
}
JERSEY_COLORS = ['Red', 'Orange', 'Yellow', 'Green', 'Blue', 'White', 'Black', 'Purple', 'Gray']


def get_sundays_for_date_range(start_date, end_date):
    start_date += datetime.timedelta(days=(6 - start_date.weekday()))
    sundays = []

    while start_date <= end_date:
        sundays.append(start_date)
        start_date += datetime.timedelta(days=7)
    return sundays


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def seed_users(count):
    print('Seeding users.')
    if User.objects.filter(is_superuser=False).exists():
        print('Users already exist.')
    else:
        users = []
        for i in range(count):
            email = person.email(unique=True, domains=['btsh.org'])
            first_name = person.first_name()
            last_name = person.last_name()
            gender = random.choice(list(User.GENDERS.keys()))

            user, _ = get_or_create(
                User,
                get_kwargs={'pk': None},
                create_kwargs={
                    'username': email,
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                    'gender': gender,
                },
                exclude=['password'],
            )
            users.append(user)
        print(f'Seeded {len(users)} users.')
    return User.objects.all().order_by('email')


def seed_divisions(division_names, created_by):
    print('Seeding divisions.')
    divisions = []
    for d in division_names:
        division, _ = get_or_create(
            Division,
            get_kwargs={'name': d},
            create_kwargs={'name': d, 'created_by': created_by}
        )
        divisions.append(division)
    print(f'Seeded {len(divisions)} divisions.')
    return Division.objects.all().order_by('name')


def seed_seasons(season_years, created_by):
    print('Seeding seasons.')
    seasons = []
    for s in season_years:
        start = datetime.date(year=s, month=3, day=1)
        end = start + datetime.timedelta(weeks=4 * 8)
        season, _ = get_or_create(
            Season,
            get_kwargs={'start': start, 'end': end},
            create_kwargs={'start': start, 'end': end, 'created_by': created_by}
        )
        seasons.append(season)
    print(f'Seeded {len(seasons)} seasons.')
    return Season.objects.all().order_by('start__year')


def seed_teams(team_names, created_by):
    print('Seeding teams.')
    teams = []
    for t in team_names:
        filename = f'{slugify(t).replace("-", "_")}.jpg'
        logo_path = settings.FIXTURES_DIR / f'team_logos/{filename}'
        with open(logo_path, 'rb') as f:
            logo = File(f, name=filename)
            jersey_colors = random.sample(JERSEY_COLORS, random.randint(1, 2))
            team, _ = get_or_create(
                Team,
                get_kwargs={'name': t},
                create_kwargs={
                    'name': t,
                    'short_name': SHORT_NAMES.get(t),
                    'logo': logo,
                    'jersey_colors': jersey_colors,
                    'created_by': created_by
                }
            )
            teams.append(team)
    print(f'Seeded {len(teams)} teams.')
    return Team.objects.all().order_by('name')


def seed_team_season_registrations(seasons, teams, divisions, created_by):
    print('Seeding team season registrations.')
    if TeamSeasonRegistration.objects.exists():
        print('Team season registrations already exist.')
    else:
        team_season_registrations = []
        for season in seasons:
            _teams = [*teams]
            random.shuffle(_teams)
            for d in divisions:
                for t in _teams[:TEAMS_PER_DIVISION]:
                    team_season_registration, _ = get_or_create(
                        TeamSeasonRegistration,
                        get_kwargs={'season': season, 'team': t},
                        create_kwargs={'season': season, 'team': t, 'division': d, 'created_by': created_by},
                    )
                    team_season_registrations.append(team_season_registration)
                # Remove the teams we just seeded so we don't add them to a different division in the season
                _teams = _teams[TEAMS_PER_DIVISION:]
        print(f'Seeded {len(team_season_registrations)} team season registrations.')
    return TeamSeasonRegistration.objects.all().order_by('season__year', 'division__name', 'team__name')


def seed_user_season_registrations(seasons, teams, users, created_by):
    print('Seeding user season registrations.')
    user_season_registrations = []
    if UserSeasonRegistration.objects.exists():
        print('User season registrations already exist.')
    else:
        for season in seasons:
            _users = [*users]
            random.shuffle(_users)
            for team in teams:
                for u in _users[:USERS_PER_TEAM]:
                    usr, _ = get_or_create(
                        UserSeasonRegistration,
                        get_kwargs={'user': u, 'team': team, 'season': season},
                        create_kwargs={
                            'user': u,
                            'season': season,
                            'team': team,
                            'is_captain': random.randint(0, 20) % 3 == 0,
                            'position': random.choice(list(UserSeasonRegistration.POSITIONS.keys())),
                            'signature': u.get_full_name(),
                            'location': random.choice(list(UserSeasonRegistration.LOCATIONS.keys())),
                            'interested_in': None,
                            'mid_season_party_ideas': None,
                            'created_by': created_by,
                        }
                    )
                    user_season_registrations.append(usr)
                _users = _users[USERS_PER_TEAM:]
        print(f'Seeded {len(user_season_registrations)} user season registrations.')
    return UserSeasonRegistration.objects.all().order_by('season__year', 'user__first_name', 'user__last_name')


def seed_games(seasons, teams, created_by):
    games = []
    for season in seasons:
        sundays = get_sundays_for_date_range(season.start, season.end)
        num_games_per_day = 10
        playoff_start_date = datetime.date(year=season.year, month=10, day=1)

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
                game_type = Game.REGULAR if game_day.day <= playoff_start_date else Game.PLAYOFF
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
                        'type': game_type,
                        'created_by': created_by,
                    },
                )
                games.append(game)
                game_number += 1

            print_separator()
    print(f'Seeded {len(games)} games.')
    return Game.objects.all()


class Command(BaseCommand):
    help = 'Seed data for local development purposes.'

    def handle(self, *args, **options):
        created_by = get_default_created_by()

        # Assume 20ish users per team
        users = seed_users(len(TEAMS) * USERS_PER_TEAM)
        print_separator()

        divisions = seed_divisions(DIVISIONS, created_by)
        print_separator()

        seasons = seed_seasons(SEASONS, created_by)
        print_separator()

        teams = seed_teams(TEAMS, created_by)
        print_separator()

        seed_team_season_registrations(seasons, teams, divisions, created_by)
        print_separator()

        seed_user_season_registrations(seasons, teams, users, created_by)
        print_separator()

        seed_games(seasons, list(teams), created_by)
        print_separator()
