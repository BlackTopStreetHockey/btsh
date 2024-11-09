from api.utils.testing import BaseTest
from games.serializers import GameDayReadOnlySerializer, GameReadOnlySerializer


class TestGameDayReadOnlySerializer(BaseTest):
    def test_serialize(self, settings, game_day1_2024, game_day1_2024_expected_json):
        s = GameDayReadOnlySerializer(game_day1_2024)

        assert s.data == game_day1_2024_expected_json(tz=settings.DEFAULT_USER_TIME_ZONE)


class TestGameReadOnlySerializer(BaseTest):
    def test_serialize(self, settings, hookers_lbs_game_day1_2024, hookers_lbs_game_day1_2024_expected_json):
        s = GameReadOnlySerializer(hookers_lbs_game_day1_2024)

        assert s.data == hookers_lbs_game_day1_2024_expected_json(tz=settings.DEFAULT_USER_TIME_ZONE, logo_prefix='')
