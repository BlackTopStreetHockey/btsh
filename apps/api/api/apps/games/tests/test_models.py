from datetime import date

import pytest
from django.core.exceptions import ValidationError


@pytest.mark.django_db
class TestGameDayModel:
    @pytest.mark.parametrize('day', [
        date(year=2023, month=2, day=1),
        date(year=2024, month=3, day=1),
        date(year=2024, month=11, day=1),
        date(year=2025, month=1, day=15),
    ])
    def test_clean(self, day, game_day_factory, season_2024, lbs, corlears_hookers):
        with pytest.raises(ValidationError) as e:
            game_day_factory(day=day, season=season_2024, opening_team=lbs, closing_team=corlears_hookers)
        assert e.value.message_dict == {
            'day': ['Day must be between 03/31/2024 and 10/31/2024.'],
        }

    def test_to_str(self, game_day1_2024):
        assert str(game_day1_2024) == '04/07/2024'


@pytest.mark.django_db
class TestGameModel:
    def test_to_str(self, hookers_lbs_game_day1_2024):
        assert str(hookers_lbs_game_day1_2024) == '04/07/2024 12:00PM Corlears Hookers vs. Lbs'

    def test_unique_constraint(self, game_factory, hookers_lbs_game_day1_2024):
        with pytest.raises(ValidationError) as e:
            game_factory(
                game_day=hookers_lbs_game_day1_2024.game_day,
                start=hookers_lbs_game_day1_2024.start,
                home_team=hookers_lbs_game_day1_2024.home_team,
                away_team=hookers_lbs_game_day1_2024.away_team,
                court=hookers_lbs_game_day1_2024.court,
                game_type=hookers_lbs_game_day1_2024.type,
            )
        assert e.value.message_dict == {
            '__all__': ['Game with this Game day, Start, Home team and Away team already exists.']
        }
