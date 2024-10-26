import pathlib
from datetime import date, time

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from divisions.models import Division
from games.models import Game, GameDay
from seasons.models import Season
from teams.models import Team


@pytest.fixture
def division_factory():
    def _factory(name):
        division = Division(name=name)
        division.full_clean()
        division.save()
        return division

    return _factory


@pytest.fixture
def division1(division_factory):
    yield division_factory(name='Division 1')


@pytest.fixture
def division2(division_factory):
    yield division_factory(name='Division 2')


@pytest.fixture
def division3(division_factory):
    yield division_factory(name='Division 3')


@pytest.fixture
def division4(division_factory):
    yield division_factory(name='Division 4')


@pytest.fixture
def season_factory():
    def _factory(start, end):
        season = Season(start=start, end=end)
        season.full_clean()
        season.save()
        return season

    return _factory


@pytest.fixture
def season_2020(season_factory):
    year = 2020
    yield season_factory(start=date(year=year, month=3, day=31), end=date(year=year, month=10, day=31))


@pytest.fixture
def season_2021(season_factory):
    year = 2021
    yield season_factory(start=date(year=year, month=3, day=31), end=date(year=year, month=10, day=31))


@pytest.fixture
def season_2022(season_factory):
    year = 2022
    yield season_factory(start=date(year=year, month=3, day=31), end=date(year=year, month=10, day=31))


@pytest.fixture
def season_2023(season_factory):
    year = 2023
    yield season_factory(start=date(year=year, month=3, day=31), end=date(year=year, month=10, day=31))


@pytest.fixture
def season_2024(season_factory):
    year = 2024
    yield season_factory(start=date(year=year, month=3, day=31), end=date(year=year, month=10, day=31))


@pytest.fixture
def team_factory():
    def _factory(name: str, logo: pathlib.Path, jersey_colors: list[str] | None):
        team = Team(
            name=name,
            logo=SimpleUploadedFile(
                logo.name,
                logo.read_bytes(),
                content_type=f'image/{logo.suffix[1:]}'
            ),
            jersey_colors=jersey_colors,
        )
        team.full_clean()
        team.save()
        return team

    return _factory


@pytest.fixture
def corlears_hookers(team_factory, settings):
    yield team_factory(
        name='Corlears Hookers',
        logo=settings.FIXTURES_DIR / 'team_logos/corlears_hookers.jpg',
        jersey_colors=['white', 'purple']
    )


@pytest.fixture
def butchers(team_factory, settings):
    yield team_factory(
        name='Butchers',
        logo=settings.FIXTURES_DIR / 'team_logos/butchers.jpg',
        jersey_colors=None,
    )


@pytest.fixture
def lbs(team_factory, settings):
    yield team_factory(
        name='Lbs',
        logo=settings.FIXTURES_DIR / 'team_logos/lbs.jpg',
        jersey_colors=None,
    )


@pytest.fixture
def cobra_kai(team_factory, settings):
    yield team_factory(
        name='Cobra Kai',
        logo=settings.FIXTURES_DIR / 'team_logos/cobra_kai.jpg',
        jersey_colors=None,
    )


@pytest.fixture
def dark_rainbows(team_factory, settings):
    yield team_factory(
        name='Dark Rainbows',
        logo=settings.FIXTURES_DIR / 'team_logos/dark_rainbows.jpg',
        jersey_colors=None,
    )


@pytest.fixture
def denim_demons(team_factory, settings):
    yield team_factory(
        name='Denim Demons',
        logo=settings.FIXTURES_DIR / 'team_logos/denim_demons.jpg',
        jersey_colors=None,
    )


@pytest.fixture
def game_day_factory():
    def _factory(day, season, opening_team, closing_team):
        game_day = GameDay(
            day=day,
            season=season,
            opening_team=opening_team,
            closing_team=closing_team,
        )
        game_day.full_clean()
        game_day.save()
        return game_day

    return _factory


@pytest.fixture
def game_day1_2024(game_day_factory, season_2024, corlears_hookers, butchers):
    yield game_day_factory(
        day=date(year=season_2024.start.year, month=season_2024.start.month + 1, day=7),
        season=season_2024,
        opening_team=butchers,
        closing_team=corlears_hookers,
    )


@pytest.fixture
def game_day2_2024(game_day_factory, season_2024, lbs, denim_demons):
    yield game_day_factory(
        day=date(year=season_2024.start.year, month=season_2024.start.month + 1, day=14),
        season=season_2024,
        opening_team=lbs,
        closing_team=denim_demons,
    )


@pytest.fixture
def game_day3_2024(game_day_factory, season_2024, dark_rainbows, corlears_hookers):
    yield game_day_factory(
        day=date(year=season_2024.start.year, month=season_2024.start.month + 1, day=21),
        season=season_2024,
        opening_team=corlears_hookers,
        closing_team=dark_rainbows,
    )


@pytest.fixture
def game_factory():
    def _factory(game_day, start, home_team, away_team, court, duration=None, location=None):
        kwargs = {
            'game_day': game_day,
            'start': start,
            'home_team': home_team,
            'away_team': away_team,
            'court': court,
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
def hookers_lbs_game_day1_2024(game_day1_2024, corlears_hookers, lbs, game_factory):
    yield game_factory(
        game_day=game_day1_2024,
        start=time(hour=12, minute=0),
        home_team=corlears_hookers,
        away_team=lbs,
        court=Game.EAST,
    )
