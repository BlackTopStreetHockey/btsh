import pathlib
from datetime import date, time

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient

from api.utils.datetime import datetime_to_drf
from divisions.models import Division
from games.models import Game, GameDay
from seasons.models import Season
from teams.models import Team, TeamSeasonRegistration
from users.models import User, UserSeasonRegistration


pytest.register_assert_rewrite('api.utils.assertions')


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
def scrosby(user_factory):
    yield user_factory(
        first_name='Sidney',
        last_name='Crosby',
        email='s.crosby@btsh.org',
        password='penguins',
        gender=User.MALE,
    )


@pytest.fixture
def akessel(user_factory):
    yield user_factory(
        first_name='Amanda',
        last_name='Kessel',
        email='a.kessel@btsh.org',
        password='philssister',
        gender=User.FEMALE,
    )


@pytest.fixture
def hknight(user_factory):
    yield user_factory(
        first_name='Hilary',
        last_name='Knight',
        email='h.knight@btsh.org',
        password='knight',
        gender=User.FEMALE,
    )


@pytest.fixture
def snurse(user_factory):
    yield user_factory(
        first_name='Sarah',
        last_name='Nurse',
        email='s.nurse@btsh.org',
        password='nurse',
        gender=User.FEMALE,
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
def division1_expected_json(division1):
    return {
        'id': division1.id,
        'name': 'Division 1',
    }


@pytest.fixture
def division2(division_factory, placeholder_user):
    yield division_factory(name='Division 2', created_by=placeholder_user)


@pytest.fixture
def division2_expected_json(division2):
    return {
        'id': division2.id,
        'name': 'Division 2',
    }


@pytest.fixture
def division3(division_factory, placeholder_user):
    yield division_factory(name='Division 3', created_by=placeholder_user)


@pytest.fixture
def division3_expected_json(division3):
    return {
        'id': division3.id,
        'name': 'Division 3',
    }


@pytest.fixture
def division4(division_factory, placeholder_user):
    yield division_factory(name='Division 4', created_by=placeholder_user)


@pytest.fixture
def division4_expected_json(division4):
    return {
        'id': division4.id,
        'name': 'Division 4',
    }


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
def season_2022_expected_json(season_2022):
    def _factory(is_past, is_current, is_future):
        return {
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
def season_2023_expected_json(season_2023):
    def _factory(is_past, is_current, is_future):
        return {
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
def season_2024_expected_json(season_2024):
    def _factory(is_past, is_current, is_future):
        return {
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
def corlears_hookers_expected_json(corlears_hookers):
    def _factory(logo_prefix=''):
        return {
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
def butchers_expected_json(butchers):
    def _factory(logo_prefix=''):
        return {
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
def lbs_expected_json(lbs):
    def _factory(logo_prefix=''):
        return {
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
def cobra_kai_expected_json(cobra_kai):
    def _factory(logo_prefix=''):
        return {
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
def dark_rainbows_expected_json(dark_rainbows):
    def _factory(logo_prefix=''):
        return {
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
def denim_demons_expected_json(denim_demons):
    def _factory(logo_prefix=''):
        return {
            'id': denim_demons.id,
            'name': 'Denim Demons',
            'short_name': 'DMNS',
            'logo': f'{logo_prefix}/media/{denim_demons.logo.name}',
            'jersey_colors': None,
        }

    return _factory


@pytest.fixture
def user_season_registration_factory():
    def _factory(user, season, team, is_captain, position, signature, location, registered_at=None,
                 interested_in_reffing=None, interested_in_opening_closing=None, interested_in_other=None,
                 interested_in_next_year=None, mid_season_party_ideas=None):
        kwargs = {
            'user': user,
            'season': season,
            'team': team,
            'is_captain': is_captain,
            'position': position,
            'signature': signature,
            'location': location,
        }

        if registered_at:
            kwargs.update({'registered_at': registered_at})

        user_season_registration = UserSeasonRegistration(
            **kwargs,
            interested_in_reffing=interested_in_reffing,
            interested_in_opening_closing=interested_in_opening_closing,
            interested_in_other=interested_in_other,
            interested_in_next_year=interested_in_next_year,
            mid_season_party_ideas=mid_season_party_ideas,
        )
        user_season_registration.full_clean()
        user_season_registration.save()
        return user_season_registration

    return _factory


@pytest.fixture
def wgretzky_2023_season_registration(user_season_registration_factory, wgretzky, season_2023, denim_demons):
    yield user_season_registration_factory(
        user=wgretzky,
        season=season_2023,
        team=denim_demons,
        is_captain=False,
        position=UserSeasonRegistration.DEFENSE,
        signature='Wayne Gretzky',
        location=UserSeasonRegistration.BRONX,
        interested_in_reffing=True,
        interested_in_opening_closing=False,
        interested_in_other='Can Mark Messier play in this league?',
        interested_in_next_year=False,
        mid_season_party_ideas=None,
    )


@pytest.fixture
def wgretzky_2024_season_registration(user_season_registration_factory, wgretzky, season_2024, corlears_hookers):
    yield user_season_registration_factory(
        user=wgretzky,
        season=season_2024,
        team=corlears_hookers,
        is_captain=True,
        position=UserSeasonRegistration.FORWARD,
        signature='Wayne Gretzky',
        location=UserSeasonRegistration.BRONX,
        interested_in_reffing=False,
        interested_in_opening_closing=False,
        interested_in_other=None,
        interested_in_next_year=False,
        mid_season_party_ideas=None,
    )


@pytest.fixture
def team_season_registration_factory():
    def _factory(season, team, division, home_games_played, away_games_played, home_regulation_wins,
                 home_regulation_losses, home_overtime_wins, home_overtime_losses, home_shootout_wins,
                 home_shootout_losses, home_ties, away_regulation_wins,
                 away_regulation_losses, away_overtime_wins, away_overtime_losses, away_shootout_wins,
                 away_shootout_losses, away_ties, home_goals_for, home_goals_against, away_goals_for,
                 away_goals_against):
        team_season_registration = TeamSeasonRegistration(
            season=season,
            team=team,
            division=division,
            home_games_played=home_games_played,
            away_games_played=away_games_played,
            home_regulation_wins=home_regulation_wins,
            home_regulation_losses=home_regulation_losses,
            home_overtime_wins=home_overtime_wins,
            home_overtime_losses=home_overtime_losses,
            home_shootout_wins=home_shootout_wins,
            home_shootout_losses=home_shootout_losses,
            home_ties=home_ties,
            away_regulation_wins=away_regulation_wins,
            away_regulation_losses=away_regulation_losses,
            away_overtime_wins=away_overtime_wins,
            away_overtime_losses=away_overtime_losses,
            away_shootout_wins=away_shootout_wins,
            away_shootout_losses=away_shootout_losses,
            away_ties=away_ties,
            home_goals_for=home_goals_for,
            home_goals_against=home_goals_against,
            away_goals_for=away_goals_for,
            away_goals_against=away_goals_against,
        )
        team_season_registration.full_clean()
        team_season_registration.save()
        return team_season_registration

    return _factory


@pytest.fixture
def corlears_hookers_2024_season_registration(team_season_registration_factory, corlears_hookers, season_2024,
                                              division4):
    yield team_season_registration_factory(
        team=corlears_hookers,
        season=season_2024,
        division=division4,
        home_games_played=7,
        away_games_played=8,
        home_regulation_wins=1,
        home_regulation_losses=1,
        home_overtime_wins=1,
        home_overtime_losses=1,
        home_shootout_wins=1,
        home_shootout_losses=1,
        home_ties=1,
        away_regulation_wins=2,
        away_regulation_losses=1,
        away_overtime_wins=1,
        away_overtime_losses=1,
        away_shootout_wins=1,
        away_shootout_losses=1,
        away_ties=1,
        home_goals_for=35,
        home_goals_against=10,
        away_goals_for=34,
        away_goals_against=15,
    )


@pytest.fixture
def corlears_hookers_2024_season_registration_expected_json(corlears_hookers_2024_season_registration,
                                                            corlears_hookers_expected_json, season_2024_expected_json,
                                                            division4_expected_json):
    def _factory(logo_prefix=''):
        return {
            'id': corlears_hookers_2024_season_registration.id,
            'team': corlears_hookers_expected_json(logo_prefix=logo_prefix),
            'season': season_2024_expected_json(is_past=True, is_current=False, is_future=False),
            'division': division4_expected_json,
            'points': None,
            'wins': None,
            'losses': None,
            'ties': None,
            'record': None,
            'point_percentage': None,
            'overtime_losses': 2,
            'shootout_losses': 2,
            'games_played': 15,
            'goals_for': 69,
            'goals_against': 25,
            'goal_differential': 44,
            'home_wins': 3,
            'home_losses': 3,
            'away_wins': 4,
            'away_losses': 3,
            'regulation_wins': 3,
            'regulation_losses': 2,
            'overtime_wins': 2,
            'shootout_wins': 2,
            'home_games_played': 7,
            'away_games_played': 8,
            'home_regulation_wins': 1,
            'home_regulation_losses': 1,
            'home_overtime_wins': 1,
            'home_overtime_losses': 1,
            'home_shootout_wins': 1,
            'home_shootout_losses': 1,
            'home_ties': 1,
            'away_regulation_wins': 2,
            'away_regulation_losses': 1,
            'away_overtime_wins': 1,
            'away_overtime_losses': 1,
            'away_shootout_wins': 1,
            'away_shootout_losses': 1,
            'away_ties': 1,
            'home_goals_for': 35,
            'home_goals_against': 10,
            'away_goals_for': 34,
            'away_goals_against': 15,
            'place': 1,
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
def game_day1_2024_expected_json(game_day1_2024, season_2024_expected_json, butchers_expected_json,
                                 corlears_hookers_expected_json):
    def _factory(logo_prefix=''):
        return {
            'id': game_day1_2024.id,
            'day': '2024-04-07',
            'season': season_2024_expected_json(is_past=True, is_current=False, is_future=False),
            'opening_team': butchers_expected_json(logo_prefix=logo_prefix),
            'closing_team': corlears_hookers_expected_json(logo_prefix=logo_prefix),
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
def hookers_lbs_game_day1_2024_expected_json(hookers_lbs_game_day1_2024, game_day1_2024_expected_json,
                                             corlears_hookers_expected_json, lbs_expected_json):
    def _factory(logo_prefix=''):
        return {
            'id': hookers_lbs_game_day1_2024.id,
            'game_day': game_day1_2024_expected_json(logo_prefix=logo_prefix),
            'start': '12:00:00',
            'duration': '00:50:00',
            'end': time(hour=12, minute=50),
            'home_team': corlears_hookers_expected_json(logo_prefix=logo_prefix),
            'away_team': lbs_expected_json(logo_prefix=logo_prefix),
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
                                                                game_day1_2024_expected_json,
                                                                denim_demons_expected_json,
                                                                dark_rainbows_expected_json):
    def _factory(logo_prefix=''):
        return {
            'id': demons_rainbows_game_day1_2024.id,
            'game_day': game_day1_2024_expected_json(logo_prefix=logo_prefix),
            'start': '12:00:00',
            'duration': '00:50:00',
            'end': time(hour=12, minute=50),
            'home_team': denim_demons_expected_json(logo_prefix=logo_prefix),
            'away_team': dark_rainbows_expected_json(logo_prefix=logo_prefix),
            'location': 'Tompkins Square Park',
            'court': 'west',
            'get_court_display': 'West',
            'type': 'regular',
            'get_type_display': 'Regular',
        }

    return _factory
