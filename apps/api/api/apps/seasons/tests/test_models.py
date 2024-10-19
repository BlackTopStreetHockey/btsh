from datetime import date, datetime, timedelta, timezone

import pytest
from django.core.exceptions import ValidationError


@pytest.mark.django_db
class TestSeasonModel:
    def test_start_formatted(self, season_2024):
        assert season_2024.start_formatted == '03/31/2024'

    def test_end_formatted(self, season_2024):
        assert season_2024.end_formatted == '10/31/2024'

    @pytest.mark.parametrize('now,expected', [
        # now is after the end date
        (datetime(year=2021, month=11, day=25, hour=11, minute=55, second=33, tzinfo=timezone.utc), True),
        # now is the same as the end date
        (datetime(year=2021, month=10, day=5, hour=9, minute=23, second=12, tzinfo=timezone.utc), False),
        # now is before the end date
        (datetime(year=2021, month=8, day=25, hour=4, minute=0, second=4, tzinfo=timezone.utc), False),
    ])
    def test_is_past(self, season_factory, mocker, now, expected):
        mocker.patch('django.utils.timezone.now', return_value=now)
        end = date(year=2021, month=10, day=5)
        start = end - timedelta(weeks=8 * 4)
        season = season_factory(start=start, end=end)
        assert season.is_past is expected

    @pytest.mark.parametrize('now,expected', [
        # now is after the start date
        (datetime(year=2021, month=11, day=25, hour=12, minute=35, second=5, tzinfo=timezone.utc), True),
        # now is the same as the start date
        (datetime(year=2021, month=10, day=5, hour=10, minute=22, second=36, tzinfo=timezone.utc), True),
        # now is before the start date
        (datetime(year=2021, month=8, day=25, hour=9, minute=12, second=33, tzinfo=timezone.utc), False),
        # now is after the end date
        (datetime(year=2022, month=5, day=17, hour=11, minute=6, second=0, tzinfo=timezone.utc), False),
        # now is the same as the end date
        (datetime(year=2022, month=4, day=5, hour=9, minute=4, second=1, tzinfo=timezone.utc), True),
        # now is before the end date
        (datetime(year=2022, month=2, day=1, hour=17, minute=3, second=8, tzinfo=timezone.utc), True),
    ])
    def test_is_current(self, season_factory, mocker, now, expected):
        mocker.patch('django.utils.timezone.now', return_value=now)
        start = date(year=2021, month=10, day=5)
        end = date(year=2022, month=4, day=5)
        season = season_factory(start=start, end=end)
        assert season.is_current is expected

    @pytest.mark.parametrize('now,expected', [
        # now is after the start date
        (datetime(year=2021, month=11, day=25, hour=22, minute=15, second=31, tzinfo=timezone.utc), False),
        # now is the same as the start date
        (datetime(year=2021, month=10, day=5, hour=11, minute=51, second=0, tzinfo=timezone.utc), False),
        # now is before the start date
        (datetime(year=2021, month=8, day=25, hour=6, minute=3, second=5, tzinfo=timezone.utc), True),
    ])
    def test_is_future(self, season_factory, mocker, now, expected):
        mocker.patch('django.utils.timezone.now', return_value=now)
        start = date(year=2021, month=10, day=5)
        end = start + timedelta(weeks=8 * 4)
        season = season_factory(start=start, end=end)
        assert season.is_future is expected

    def test_clean(self, season_factory):
        with pytest.raises(ValidationError) as e:
            season_factory(start=date(year=2020, month=2, day=1), end=date(2019, month=4, day=2))
        assert e.value.message_dict == {
            'start': ['Start date must be before end date.'],
            'end': ['End date must be after start date.'],
        }

    def test_to_str(self, season_2024):
        assert str(season_2024) == '03/31/2024 - 10/31/2024 Season'

    def test_start_end_uniq(self, season_factory):
        start = date(year=2020, month=3, day=1)
        end = start + timedelta(weeks=4 * 8)

        season_factory(start=start, end=end)

        with pytest.raises(ValidationError) as e:
            season_factory(start=start, end=end)
        assert e.value.message_dict == {
            '__all__': ['Season with this Start and End already exists.']
        }
