import pathlib
from datetime import date, time

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient

from api.utils.datetime import datetime_to_drf
from divisions.models import Division
from games.models import Game, GameDay
from seasons.models import Season
from teams.models import Team
from users.models import User


@pytest.fixture
def api_client():
    yield APIClient()


@pytest.fixture
def user_factory():
    def _factory(first_name, last_name, email, password, gender):
        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=email,
            email=email,
            password=password,
            gender=gender,
        )

    return _factory


@pytest.fixture
def placeholder_user(user_factory):
    yield user_factory(
        first_name='Michael',
        last_name='Scott',
        email='mscott@dundermifflin.com',
        password='ilovepaper',
        gender=User.MALE,
    )


@pytest.fixture
def placeholder_user_expected_json(placeholder_user):
    def _factory(tz=None):
        return {
            'id': placeholder_user.id,
            'first_name': 'Michael',
            'last_name': 'Scott',
            'full_name': 'Michael Scott',
            'date_joined': datetime_to_drf(placeholder_user.date_joined, tz=tz),
        }

    return _factory


@pytest.fixture
def wgretzky(user_factory):
    yield user_factory(
        first_name='Wayne',
        last_name='Gretzky',
        email='thegr81@btsh.org',
        password='goat',
        gender=User.MALE,
    )


@pytest.fixture
def cmcdavid(user_factory):
    yield user_factory(
        first_name='Connor',
        last_name='McDavid',
        email='mcjesus@btsh.org',
        password='mcjesus',
        gender=User.MALE,
    )


@pytest.fixture
def division_factory():
    def _factory(name, created_by=None, updated_by=None):
        division = Division(name=name, created_by=created_by, updated_by=updated_by)
        division.full_clean()
        division.save()
        return division

    return _factory


@pytest.fixture
def division1(division_factory, placeholder_user):
    yield division_factory(name='Division 1', created_by=placeholder_user)


@pytest.fixture
def division2(division_factory, placeholder_user):
    yield division_factory(name='Division 2', created_by=placeholder_user)


@pytest.fixture
def division3(division_factory, placeholder_user):
    yield division_factory(name='Division 3', created_by=placeholder_user)


@pytest.fixture
def division4(division_factory, placeholder_user):
    yield division_factory(name='Division 4', created_by=placeholder_user)


@pytest.fixture
def season_factory():
    def _factory(start, end, created_by=None, updated_by=None):
        season = Season(start=start, end=end, created_by=created_by, updated_by=updated_by)
        season.full_clean()
        season.save()
        return season

    return _factory


@pytest.fixture
def season_2020(season_factory, placeholder_user):
    year = 2020
    yield season_factory(
        start=date(year=year, month=3, day=31),
        end=date(year=year, month=10, day=31),
        created_by=placeholder_user,
    )


@pytest.fixture
def season_2021(season_factory, placeholder_user):
    year = 2021
    yield season_factory(
        start=date(year=year, month=3, day=31),
        end=date(year=year, month=10, day=31),
        created_by=placeholder_user,
    )


@pytest.fixture
def season_2022(season_factory, placeholder_user):
    year = 2022
    yield season_factory(
        start=date(year=year, month=3, day=31),
        end=date(year=year, month=10, day=31),
        created_by=placeholder_user,
    )


@pytest.fixture
def season_2022_expected_json(season_2022, placeholder_user_expected_json):
    def _factory(is_past, is_current, is_future, tz=None):
        return {
            'created_by': placeholder_user_expected_json(tz),
            'updated_by': None,
            'created_at': datetime_to_drf(season_2022.created_at, tz=tz),
            'updated_at': datetime_to_drf(season_2022.updated_at, tz=tz),
            'id': season_2022.id,
            'start': '2022-03-31',
            'end': '2022-10-31',
            'is_past': is_past,
            'is_current': is_current,
            'is_future': is_future,
            'year': 2022,
        }

    return _factory


@pytest.fixture
def season_2023(season_factory, placeholder_user):
    year = 2023
    yield season_factory(
        start=date(year=year, month=3, day=31),
        end=date(year=year, month=10, day=31),
        created_by=placeholder_user,
    )


@pytest.fixture
def season_2023_expected_json(season_2023, placeholder_user_expected_json):
    def _factory(is_past, is_current, is_future, tz=None):
        return {
            'created_by': placeholder_user_expected_json(tz),
            'updated_by': None,
            'created_at': datetime_to_drf(season_2023.created_at, tz=tz),
            'updated_at': datetime_to_drf(season_2023.updated_at, tz=tz),
            'id': season_2023.id,
            'start': '2023-03-31',
            'end': '2023-10-31',
            'is_past': is_past,
            'is_current': is_current,
            'is_future': is_future,
            'year': 2023,
        }

    return _factory


@pytest.fixture
def season_2024(season_factory, placeholder_user):
    year = 2024
    yield season_factory(
        start=date(year=year, month=3, day=31),
        end=date(year=year, month=10, day=31),
        created_by=placeholder_user,
    )


@pytest.fixture
def season_2024_expected_json(season_2024, placeholder_user_expected_json):
    def _factory(is_past, is_current, is_future, tz=None):
        return {
            'created_by': placeholder_user_expected_json(tz),
            'updated_by': None,
            'created_at': datetime_to_drf(season_2024.created_at, tz=tz),
            'updated_at': datetime_to_drf(season_2024.updated_at, tz=tz),
            'id': season_2024.id,
            'start': '2024-03-31',
            'end': '2024-10-31',
            'is_past': is_past,
            'is_current': is_current,
            'is_future': is_future,
            'year': 2024,
        }

    return _factory


@pytest.fixture
def team_factory():
    def _factory(name: str, short_name: str, logo: pathlib.Path, jersey_colors: list[str] | None, created_by=None,
                 updated_by=None):
        team = Team(
            name=name,
            short_name=short_name,
            logo=SimpleUploadedFile(
                logo.name,
                logo.read_bytes(),
                content_type=f'image/{logo.suffix[1:]}'
            ),
            jersey_colors=jersey_colors,
            created_by=created_by,
            updated_by=updated_by,
        )
        team.full_clean()
        team.save()
        return team

    return _factory


@pytest.fixture
def corlears_hookers(team_factory, settings, placeholder_user):
    yield team_factory(
        name='Corlears Hookers',
        short_name='HOOK',
        logo=settings.FIXTURES_DIR / 'team_logos/corlears_hookers.jpg',
        jersey_colors=['white', 'purple'],
        created_by=placeholder_user,
    )


@pytest.fixture
def corlears_hookers_expected_json(corlears_hookers, placeholder_user_expected_json):
    def _factory(tz=None, logo_prefix=''):
        return {
            'created_by': placeholder_user_expected_json(tz),
            'updated_by': None,
            'created_at': datetime_to_drf(corlears_hookers.created_at, tz=tz),
            'updated_at': datetime_to_drf(corlears_hookers.updated_at, tz=tz),
            'id': corlears_hookers.id,
            'name': 'Corlears Hookers',
            'short_name': 'HOOK',
            'logo': f'{logo_prefix}/media/{corlears_hookers.logo.name}',
            'jersey_colors': ['white', 'purple'],
        }

    return _factory


@pytest.fixture
def butchers(team_factory, settings, placeholder_user):
    yield team_factory(
        name='Butchers',
        short_name='BUTCH',
        logo=settings.FIXTURES_DIR / 'team_logos/butchers.jpg',
        jersey_colors=None,
        created_by=placeholder_user,
    )


@pytest.fixture
def butchers_expected_json(butchers, placeholder_user_expected_json):
    def _factory(tz=None, logo_prefix=''):
        return {
            'created_by': placeholder_user_expected_json(tz),
            'updated_by': None,
            'created_at': datetime_to_drf(butchers.created_at, tz=tz),
            'updated_at': datetime_to_drf(butchers.updated_at, tz=tz),
            'id': butchers.id,
            'name': 'Butchers',
            'short_name': 'BUTCH',
            'logo': f'{logo_prefix}/media/{butchers.logo.name}',
            'jersey_colors': None,
        }

    return _factory


@pytest.fixture
def lbs(team_factory, settings, placeholder_user):
    yield team_factory(
        name='Lbs',
        short_name='LBS',
        logo=settings.FIXTURES_DIR / 'team_logos/lbs.jpg',
        jersey_colors=None,
        created_by=placeholder_user,
    )


@pytest.fixture
def lbs_expected_json(lbs, placeholder_user_expected_json):
    def _factory(tz=None, logo_prefix=''):
        return {
            'created_by': placeholder_user_expected_json(tz),
            'updated_by': None,
            'created_at': datetime_to_drf(lbs.created_at, tz=tz),
            'updated_at': datetime_to_drf(lbs.updated_at, tz=tz),
            'id': lbs.id,
            'name': 'Lbs',
            'short_name': 'LBS',
            'logo': f'{logo_prefix}/media/{lbs.logo.name}',
            'jersey_colors': None,
        }

    return _factory


@pytest.fixture
def cobra_kai(team_factory, settings, placeholder_user):
    yield team_factory(
        name='Cobra Kai',
        short_name='CK',
        logo=settings.FIXTURES_DIR / 'team_logos/cobra_kai.jpg',
        jersey_colors=None,
        created_by=placeholder_user,
    )


@pytest.fixture
def cobra_kai_expected_json(cobra_kai, placeholder_user_expected_json):
    def _factory(tz=None, logo_prefix=''):
        return {
            'created_by': placeholder_user_expected_json(tz),
            'updated_by': None,
            'created_at': datetime_to_drf(cobra_kai.created_at, tz=tz),
            'updated_at': datetime_to_drf(cobra_kai.updated_at, tz=tz),
            'id': cobra_kai.id,
            'name': 'Cobra Kai',
            'short_name': 'CK',
            'logo': f'{logo_prefix}/media/{cobra_kai.logo.name}',
            'jersey_colors': None,
        }

    return _factory


@pytest.fixture
def dark_rainbows(team_factory, settings, placeholder_user):
    yield team_factory(
        name='Dark Rainbows',
        short_name='DRKRNBW',
        logo=settings.FIXTURES_DIR / 'team_logos/dark_rainbows.jpg',
        jersey_colors=None,
        created_by=placeholder_user,
    )


@pytest.fixture
def dark_rainbows_expected_json(dark_rainbows, placeholder_user_expected_json):
    def _factory(tz=None, logo_prefix=''):
        return {
            'created_by': placeholder_user_expected_json(tz),
            'updated_by': None,
            'created_at': datetime_to_drf(dark_rainbows.created_at, tz=tz),
            'updated_at': datetime_to_drf(dark_rainbows.updated_at, tz=tz),
            'id': dark_rainbows.id,
            'name': 'Dark Rainbows',
            'short_name': 'DRKRNBW',
            'logo': f'{logo_prefix}/media/{dark_rainbows.logo.name}',
            'jersey_colors': None,
        }

    return _factory


@pytest.fixture
def denim_demons(team_factory, settings, placeholder_user):
    yield team_factory(
        name='Denim Demons',
        short_name='DMNS',
        logo=settings.FIXTURES_DIR / 'team_logos/denim_demons.jpg',
        jersey_colors=None,
        created_by=placeholder_user,
    )


@pytest.fixture
def denim_demons_expected_json(denim_demons, placeholder_user_expected_json):
    def _factory(tz=None, logo_prefix=''):
        return {
            'created_by': placeholder_user_expected_json(tz),
            'updated_by': None,
            'created_at': datetime_to_drf(denim_demons.created_at, tz=tz),
            'updated_at': datetime_to_drf(denim_demons.updated_at, tz=tz),
            'id': denim_demons.id,
            'name': 'Denim Demons',
            'short_name': 'DMNS',
            'logo': f'{logo_prefix}/media/{denim_demons.logo.name}',
            'jersey_colors': None,
        }

    return _factory


@pytest.fixture
def game_day_factory():
    def _factory(day, season, opening_team, closing_team, created_by=None, updated_by=None):
        game_day = GameDay(
            day=day,
            season=season,
            opening_team=opening_team,
            closing_team=closing_team,
            created_by=created_by,
            updated_by=updated_by,
        )
        game_day.full_clean()
        game_day.save()
        return game_day

    return _factory


@pytest.fixture
def game_day1_2024(game_day_factory, season_2024, corlears_hookers, butchers, placeholder_user):
    yield game_day_factory(
        day=date(year=season_2024.start.year, month=season_2024.start.month + 1, day=7),
        season=season_2024,
        opening_team=butchers,
        closing_team=corlears_hookers,
        created_by=placeholder_user,
    )


@pytest.fixture
def game_day1_2024_expected_json(game_day1_2024, placeholder_user_expected_json, season_2024_expected_json,
                                 butchers_expected_json, corlears_hookers_expected_json):
    def _factory(tz=None, logo_prefix=''):
        return {
            'created_by': placeholder_user_expected_json(tz),
            'updated_by': None,
            'created_at': datetime_to_drf(game_day1_2024.created_at, tz=tz),
            'updated_at': datetime_to_drf(game_day1_2024.updated_at, tz=tz),
            'id': game_day1_2024.id,
            'day': '2024-04-07',
            'season': season_2024_expected_json(
                is_past=True, is_current=False, is_future=False, tz=tz
            ),
            'opening_team': butchers_expected_json(tz=tz, logo_prefix=logo_prefix),
            'closing_team': corlears_hookers_expected_json(tz=tz, logo_prefix=logo_prefix),
        }

    return _factory


@pytest.fixture
def game_day2_2024(game_day_factory, season_2024, lbs, denim_demons, placeholder_user):
    yield game_day_factory(
        day=date(year=season_2024.start.year, month=season_2024.start.month + 1, day=14),
        season=season_2024,
        opening_team=lbs,
        closing_team=denim_demons,
        created_by=placeholder_user,
    )


@pytest.fixture
def game_day3_2024(game_day_factory, season_2024, dark_rainbows, corlears_hookers, placeholder_user):
    yield game_day_factory(
        day=date(year=season_2024.start.year, month=season_2024.start.month + 1, day=21),
        season=season_2024,
        opening_team=corlears_hookers,
        closing_team=dark_rainbows,
        created_by=placeholder_user,
    )


@pytest.fixture
def game_factory():
    def _factory(game_day, start, home_team, away_team, court, game_type, duration=None, location=None, created_by=None,
                 updated_by=None):
        kwargs = {
            'game_day': game_day,
            'start': start,
            'home_team': home_team,
            'away_team': away_team,
            'court': court,
            'type': game_type,
            'created_by': created_by,
            'updated_by': updated_by,
        }
        if duration is not None:
            kwargs.update({'duration': duration})
        if location is not None:
            kwargs.update({'location': location})

        game = Game(**kwargs)
        game.full_clean()
        game.save()
        return game

    return _factory


@pytest.fixture
def hookers_lbs_game_day1_2024(game_day1_2024, corlears_hookers, lbs, game_factory, placeholder_user):
    yield game_factory(
        game_day=game_day1_2024,
        start=time(hour=12, minute=0),
        home_team=corlears_hookers,
        away_team=lbs,
        court=Game.EAST,
        game_type=Game.REGULAR,
        created_by=placeholder_user,
    )


@pytest.fixture
def hookers_lbs_game_day1_2024_expected_json(hookers_lbs_game_day1_2024, placeholder_user_expected_json,
                                             game_day1_2024_expected_json, corlears_hookers_expected_json,
                                             lbs_expected_json):
    def _factory(tz=None, logo_prefix=''):
        return {
            'created_by': placeholder_user_expected_json(tz),
            'updated_by': None,
            'created_at': datetime_to_drf(hookers_lbs_game_day1_2024.created_at, tz=tz),
            'updated_at': datetime_to_drf(hookers_lbs_game_day1_2024.updated_at, tz=tz),
            'id': hookers_lbs_game_day1_2024.id,
            'game_day': game_day1_2024_expected_json(tz=tz, logo_prefix=logo_prefix),
            'start': '12:00:00',
            'duration': '00:50:00',
            'end': time(hour=12, minute=50),
            'home_team': corlears_hookers_expected_json(tz=tz, logo_prefix=logo_prefix),
            'away_team': lbs_expected_json(tz=tz, logo_prefix=logo_prefix),
            'location': 'Tompkins Square Park',
            'court': 'east',
            'get_court_display': 'East',
            'type': 'regular',
            'get_type_display': 'Regular',
        }

    return _factory


@pytest.fixture
def demons_rainbows_game_day1_2024(game_day1_2024, denim_demons, dark_rainbows, game_factory, placeholder_user):
    yield game_factory(
        game_day=game_day1_2024,
        start=time(hour=12, minute=0),
        home_team=denim_demons,
        away_team=dark_rainbows,
        court=Game.WEST,
        game_type=Game.REGULAR,
        created_by=placeholder_user,
    )


@pytest.fixture
def demons_rainbows_game_day1_2024_game_day1_2024_expected_json(demons_rainbows_game_day1_2024,
                                                                placeholder_user_expected_json,
                                                                game_day1_2024_expected_json,
                                                                denim_demons_expected_json,
                                                                dark_rainbows_expected_json):
    def _factory(tz=None, logo_prefix=''):
        return {
            'created_by': placeholder_user_expected_json(tz),
            'updated_by': None,
            'created_at': datetime_to_drf(demons_rainbows_game_day1_2024.created_at, tz=tz),
            'updated_at': datetime_to_drf(demons_rainbows_game_day1_2024.updated_at, tz=tz),
            'id': demons_rainbows_game_day1_2024.id,
            'game_day': game_day1_2024_expected_json(tz=tz, logo_prefix=logo_prefix),
            'start': '12:00:00',
            'duration': '00:50:00',
            'end': time(hour=12, minute=50),
            'home_team': denim_demons_expected_json(tz=tz, logo_prefix=logo_prefix),
            'away_team': dark_rainbows_expected_json(tz=tz, logo_prefix=logo_prefix),
            'location': 'Tompkins Square Park',
            'court': 'west',
            'get_court_display': 'West',
            'type': 'regular',
            'get_type_display': 'Regular',
        }

    return _factory
