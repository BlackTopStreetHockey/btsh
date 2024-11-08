from api.utils.testing import BaseTest
from games.serializers import GameDayReadOnlySerializer


class TestGameDayReadOnlySerializer(BaseTest):
    def test_serialize(self, settings, game_day1_2024, season_2024_expected_json, butchers_expected_json,
                       corlears_hookers_expected_json, placeholder_user_expected_json):
        s = GameDayReadOnlySerializer(game_day1_2024)

        assert s.data == {
            'created_by': placeholder_user_expected_json(settings.DEFAULT_USER_TIME_ZONE),
            'updated_by': None,
            'created_at': self.format_datetime(game_day1_2024.created_at, tz=settings.DEFAULT_USER_TIME_ZONE),
            'updated_at': self.format_datetime(game_day1_2024.updated_at, tz=settings.DEFAULT_USER_TIME_ZONE),
            'id': game_day1_2024.id,
            'day': '2024-04-07',
            'season': season_2024_expected_json(
                is_past=True, is_current=False, is_future=False, tz=settings.DEFAULT_USER_TIME_ZONE
            ),
            'opening_team': butchers_expected_json(tz=settings.DEFAULT_USER_TIME_ZONE),
            'closing_team': corlears_hookers_expected_json(tz=settings.DEFAULT_USER_TIME_ZONE),
        }
