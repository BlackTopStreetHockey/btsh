from datetime import date

import pytest

from divisions.models import Division
from seasons.models import Season


@pytest.fixture
def division_factory():
    def _factory(name):
        return Division.objects.create(name=name)

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
        return Season.objects.create(start=start, end=end)

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
