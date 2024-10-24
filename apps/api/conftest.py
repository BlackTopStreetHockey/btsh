import pathlib
from datetime import date

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from divisions.models import Division
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
