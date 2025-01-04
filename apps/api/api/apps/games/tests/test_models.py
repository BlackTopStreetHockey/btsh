from datetime import date

import pytest
from django.core.exceptions import ValidationError

from api.utils.testing import BaseTest
from games.models import Game, GameGoal


class TestGameDayModel(BaseTest):
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


class TestGameModel(BaseTest):
    def test_get_team_display(self, corlears_hookers, lbs, hookers_lbs_game_day1_2024):
        # Scheduled game
        assert hookers_lbs_game_day1_2024._get_team_display(corlears_hookers, 0) == 'Corlears Hookers'

        # Completed game
        hookers_lbs_game_day1_2024.status = Game.COMPLETED
        hookers_lbs_game_day1_2024.save()

        # Winner
        hookers_lbs_game_day1_2024.winning_team_id = corlears_hookers.id
        hookers_lbs_game_day1_2024.losing_team_id = lbs.id
        assert hookers_lbs_game_day1_2024._get_team_display(corlears_hookers, 2) == 'Corlears Hookers (2) - W'

        # Loser
        hookers_lbs_game_day1_2024.winning_team_id = lbs.id
        hookers_lbs_game_day1_2024.losing_team_id = corlears_hookers.id
        assert hookers_lbs_game_day1_2024._get_team_display(corlears_hookers, 2) == 'Corlears Hookers (2) - L'

        # Tie
        hookers_lbs_game_day1_2024.winning_team_id = None
        hookers_lbs_game_day1_2024.losing_team_id = None
        assert hookers_lbs_game_day1_2024._get_team_display(corlears_hookers, 2) == 'Corlears Hookers (2) - T'

    def test_get_team_season_registration(self, corlears_hookers, lbs, hookers_lbs_game_day1_2024,
                                          corlears_hookers_2024_season_registration):
        assert hookers_lbs_game_day1_2024.get_team_season_registration(lbs) is None
        assert (
            hookers_lbs_game_day1_2024.get_team_season_registration(corlears_hookers) ==
            corlears_hookers_2024_season_registration
        )

    def test_get_team_division(self, corlears_hookers, lbs, hookers_lbs_game_day1_2024,
                               corlears_hookers_2024_season_registration, division4):
        assert hookers_lbs_game_day1_2024._get_team_division(lbs) is None
        assert hookers_lbs_game_day1_2024._get_team_division(corlears_hookers) == division4

    def test_teams(self, corlears_hookers, lbs, hookers_lbs_game_day1_2024):
        assert hookers_lbs_game_day1_2024.teams == [corlears_hookers, lbs]

    def test_home_team_division(self, hookers_lbs_game_day1_2024, corlears_hookers_2024_season_registration, division4):
        assert hookers_lbs_game_day1_2024.home_team_division == division4

    def test_away_team_division(self, hookers_lbs_game_day1_2024, lbs_2024_season_registration, division1):
        assert hookers_lbs_game_day1_2024.away_team_division == division1

    def test_home_team_display(self, corlears_hookers, lbs, hookers_lbs_game_day1_2024):
        hookers_lbs_game_day1_2024.status = Game.COMPLETED
        hookers_lbs_game_day1_2024.save()
        hookers_lbs_game_day1_2024.winning_team_id = corlears_hookers.id
        hookers_lbs_game_day1_2024.losing_team_id = lbs.id
        hookers_lbs_game_day1_2024.home_team_num_goals = 8
        assert hookers_lbs_game_day1_2024.home_team_display == 'Corlears Hookers (8) - W'

    def test_away_team_display(self, corlears_hookers, lbs, hookers_lbs_game_day1_2024):
        hookers_lbs_game_day1_2024.status = Game.COMPLETED
        hookers_lbs_game_day1_2024.save()
        hookers_lbs_game_day1_2024.winning_team_id = corlears_hookers.id
        hookers_lbs_game_day1_2024.losing_team_id = lbs.id
        hookers_lbs_game_day1_2024.away_team_num_goals = 0
        assert hookers_lbs_game_day1_2024.away_team_display == 'Lbs (0) - L'

    def test_save(self, mocker, hookers_lbs_game_day1_2024):
        mock_calc = mocker.patch('games.models.calculate_team_season_registration_stats_from_game')

        hookers_lbs_game_day1_2024.location = 'Chelsea Piers'
        hookers_lbs_game_day1_2024.save()

        mock_calc.assert_called_with(hookers_lbs_game_day1_2024)

    def test_delete(self, mocker, hookers_lbs_game_day1_2024):
        mock_calc = mocker.patch('games.models.calculate_team_season_registration_stats_from_game')

        hookers_lbs_game_day1_2024.delete()

        mock_calc.assert_called_with(hookers_lbs_game_day1_2024)

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
                status=hookers_lbs_game_day1_2024.status,
            )
        assert e.value.message_dict == {
            '__all__': ['Game with this Game day, Start, Home team and Away team already exists.']
        }


class TestGameRefereeModel(BaseTest):
    def test_to_str(self, pbeasley_hookers_lbs_game_day1_2024_game_ref):
        assert (
            str(pbeasley_hookers_lbs_game_day1_2024_game_ref) ==
            'Pam Beasley - 04/07/2024 12:00PM Corlears Hookers vs. Lbs'
        )

    def test_game_user_type_uniq(self, game_referee_factory, pbeasley_hookers_lbs_game_day1_2024_game_ref):
        with pytest.raises(ValidationError) as e:
            game_referee_factory(
                game=pbeasley_hookers_lbs_game_day1_2024_game_ref.game,
                user=pbeasley_hookers_lbs_game_day1_2024_game_ref.user,
                _type=pbeasley_hookers_lbs_game_day1_2024_game_ref.type,
            )
        assert e.value.message_dict == {'__all__': ['Game referee with this Game, User and Type already exists.']}


class TestGamePlayerModel(BaseTest):
    def test_clean(self, game_player_factory, snurse, denim_demons, hookers_lbs_game_day1_2024, ):
        with pytest.raises(ValidationError):
            game_player_factory(
                game=None,
                user=None,
                team=None,
                is_substitute=None,
                is_goalie=None,
            )

        with pytest.raises(ValidationError) as e:
            game_player_factory(
                game=hookers_lbs_game_day1_2024,
                user=snurse,
                team=denim_demons,
                is_substitute=True,
                is_goalie=False,
            )
        assert e.value.message_dict == {'team': ['Team must be Corlears Hookers or Lbs.']}

    def test_to_str(self, wgretzky_hookers_lbs_game_day1_2024_game_player):
        assert (
            str(wgretzky_hookers_lbs_game_day1_2024_game_player) ==
            'Wayne Gretzky - Corlears Hookers - 04/07/2024 12:00PM Corlears Hookers vs. Lbs'
        )

    def test_game_user_team_uniq(self, game_player_factory, wgretzky_hookers_lbs_game_day1_2024_game_player):
        with pytest.raises(ValidationError) as e:
            game_player_factory(
                game=wgretzky_hookers_lbs_game_day1_2024_game_player.game,
                user=wgretzky_hookers_lbs_game_day1_2024_game_player.user,
                team=wgretzky_hookers_lbs_game_day1_2024_game_player.team,
                is_substitute=True,
                is_goalie=True,
            )
        assert e.value.message_dict == {'__all__': ['Game player with this Game, User and Team already exists.']}


class TestGameGoalModel(BaseTest):
    def test_validate_game_player(self, game_goal_factory, corlears_hookers, lbs, hookers_lbs_game_day1_2024,
                                  akessel_demons_rainbows_game_day1_2024_game_player):
        with pytest.raises(ValidationError) as e:
            game_goal_factory(
                game=hookers_lbs_game_day1_2024,
                team=corlears_hookers,
                team_against=lbs,
                period=GameGoal.FIRST,
                scored_by=akessel_demons_rainbows_game_day1_2024_game_player,
                assisted_by1=akessel_demons_rainbows_game_day1_2024_game_player,
                assisted_by2=akessel_demons_rainbows_game_day1_2024_game_player,
            )
        expected = [
            'This player does not belong to the selected game.',
            'This player does not belong to the selected team.',
        ]
        assert e.value.message_dict == {
            'scored_by': expected,
            'assisted_by1': ['This player can\'t be selected more than once.', *expected],
            'assisted_by2': ['This player can\'t be selected more than once.', *expected],
        }

    def test_validate_game_players(self, game_goal_factory, corlears_hookers, lbs, hookers_lbs_game_day1_2024,
                                   wgretzky_hookers_lbs_game_day1_2024_game_player):
        with pytest.raises(ValidationError) as e:
            game_goal_factory(
                game=hookers_lbs_game_day1_2024,
                team=corlears_hookers,
                team_against=lbs,
                period=GameGoal.FIRST,
                scored_by=wgretzky_hookers_lbs_game_day1_2024_game_player,
                assisted_by1=wgretzky_hookers_lbs_game_day1_2024_game_player,
                assisted_by2=wgretzky_hookers_lbs_game_day1_2024_game_player,
            )
        assert e.value.message_dict == {
            'assisted_by1': ['This player can\'t be selected more than once.'],
            'assisted_by2': ['This player can\'t be selected more than once.'],
        }

    def test_clean(self, game_goal_factory, corlears_hookers, lbs, denim_demons, hookers_lbs_game_day1_2024,
                   wgretzky_hookers_lbs_game_day1_2024_game_player, cmcdavid_hookers_lbs_game_day1_2024_game_player):
        with pytest.raises(ValidationError):
            game_goal_factory(
                game=None,
                team=None,
                team_against=None,
                period=None,
                scored_by=None,
                assisted_by1=None,
                assisted_by2=None,
            )

        # Validate team is the game home or away team
        with pytest.raises(ValidationError) as e:
            game_goal_factory(
                game=hookers_lbs_game_day1_2024,
                team=denim_demons,
                team_against=lbs,
                period=GameGoal.SECOND,
                scored_by=wgretzky_hookers_lbs_game_day1_2024_game_player,
                assisted_by1=None,
                assisted_by2=None,
            )
        assert e.value.message_dict == {
            'scored_by': ['This player does not belong to the selected team.'],
            'team': ['Team must be Corlears Hookers or Lbs.'],
        }

        # Validate team against is the game home or away team
        with pytest.raises(ValidationError) as e:
            game_goal_factory(
                game=hookers_lbs_game_day1_2024,
                team=corlears_hookers,
                team_against=denim_demons,
                period=GameGoal.SECOND,
                scored_by=wgretzky_hookers_lbs_game_day1_2024_game_player,
                assisted_by1=None,
                assisted_by2=None,
            )
        assert e.value.message_dict == {
            'team_against': ['Team must be Corlears Hookers or Lbs.'],
        }

        # Validate team is different from team against
        with pytest.raises(ValidationError) as e:
            game_goal_factory(
                game=hookers_lbs_game_day1_2024,
                team=corlears_hookers,
                team_against=corlears_hookers,
                period=GameGoal.SECOND,
                scored_by=wgretzky_hookers_lbs_game_day1_2024_game_player,
                assisted_by1=None,
                assisted_by2=None,
            )
        assert e.value.message_dict == {
            'team': ['Team must be different from team against.'],
            'team_against': ['Team against must be different from team.'],
        }

        # Validate primary assisted provided when secondary assist provided
        with pytest.raises(ValidationError) as e:
            game_goal_factory(
                game=hookers_lbs_game_day1_2024,
                team=corlears_hookers,
                team_against=lbs,
                period=GameGoal.SECOND,
                scored_by=wgretzky_hookers_lbs_game_day1_2024_game_player,
                assisted_by1=None,
                assisted_by2=cmcdavid_hookers_lbs_game_day1_2024_game_player,
            )
        assert e.value.message_dict == {
            'assisted_by1': ['This field is required when a secondary assist is provided.'],
        }

    def test_save(self, mocker, hookers_lbs_game_day1_2024_game_goal1):
        mock_calc = mocker.patch('games.models.calculate_team_season_registration_stats_from_game')

        hookers_lbs_game_day1_2024_game_goal1.period = GameGoal.SECOND
        hookers_lbs_game_day1_2024_game_goal1.save()

        mock_calc.assert_called_with(game=hookers_lbs_game_day1_2024_game_goal1.game, statuses=[Game.COMPLETED])

    def test_delete(self, mocker, hookers_lbs_game_day1_2024_game_goal1):
        mock_calc = mocker.patch('games.models.calculate_team_season_registration_stats_from_game')

        hookers_lbs_game_day1_2024_game_goal1.delete()

        mock_calc.assert_called_with(game=hookers_lbs_game_day1_2024_game_goal1.game, statuses=[Game.COMPLETED])

    def test_to_str(self, hookers_lbs_game_day1_2024_game_goal1):
        assert (
            str(hookers_lbs_game_day1_2024_game_goal1) ==
            'Wayne Gretzky - Corlears Hookers - 04/07/2024 12:00PM Corlears Hookers vs. Lbs'
        )
