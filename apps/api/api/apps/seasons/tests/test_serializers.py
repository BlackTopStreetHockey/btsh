from datetime import datetime, timezone

from api.utils.testing import BaseTest
from seasons.serializers import SeasonReadOnlySerializer


class TestSeasonReadOnlySerializer(BaseTest):
    def test_serialize(self, mocker, settings, season_2024, season_2024_expected_json):
        mocker.patch('django.utils.timezone.now', return_value=datetime(
            year=season_2024.start.year,
            month=5,
            day=20,
            hour=12,
            minute=3,
            second=9,
            tzinfo=timezone.utc,
        ))

        s = SeasonReadOnlySerializer(season_2024)

        assert s.data == season_2024_expected_json(
            is_past=False, is_current=True, is_future=False, tz=settings.DEFAULT_USER_TIME_ZONE,
        )
