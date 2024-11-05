from datetime import datetime, timezone

from api.utils.testing import BaseTest
from seasons.serializers import SeasonReadOnlySerializer


class TestSeasonReadOnlySerializer(BaseTest):
    def test_serialize(self, mocker, settings, season_2024, placeholder_user_expected_json):
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

        assert s.data == {
            'created_by': placeholder_user_expected_json(settings.DEFAULT_USER_TIME_ZONE),
            'updated_by': None,
            'created_at': self.format_datetime(season_2024.created_at, tz=settings.DEFAULT_USER_TIME_ZONE),
            'updated_at': self.format_datetime(season_2024.updated_at, tz=settings.DEFAULT_USER_TIME_ZONE),
            'id': season_2024.id,
            'start': '2024-03-31',
            'end': '2024-10-31',
            'is_past': False,
            'is_current': True,
            'is_future': False,
        }
