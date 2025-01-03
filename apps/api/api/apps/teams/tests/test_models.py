import pytest
from django.core.exceptions import ValidationError

from api.utils.testing import BaseTest


class TestTeamModel(BaseTest):
    def test_to_str(self, corlears_hookers):
        assert str(corlears_hookers) == 'Corlears Hookers'


class TestTeamSeasonRegistrationModel(BaseTest):
    def test_generated_fields(self, team_season_registration_factory, season_2024, corlears_hookers, division4):
        tsr = team_season_registration_factory(
            season=season_2024,
            team=corlears_hookers,
            division=division4,
            home_games_played=7,
            away_games_played=8,
            home_regulation_wins=1,
            home_regulation_losses=1,
            home_overtime_wins=1,
            home_overtime_losses=1,
            home_shootout_wins=1,
            home_shootout_losses=1,
            home_ties=1,
            away_regulation_wins=2,
            away_regulation_losses=1,
            away_overtime_wins=1,
            away_overtime_losses=1,
            away_shootout_wins=1,
            away_shootout_losses=1,
            away_ties=1,
            home_goals_for=35,
            home_goals_against=10,
            away_goals_for=34,
            away_goals_against=15,
        )

        assert tsr.games_played == 15
        assert tsr.home_wins == 3
        assert tsr.home_losses == 3
        assert tsr.away_wins == 4
        assert tsr.away_losses == 3
        assert tsr.regulation_wins == 3
        assert tsr.regulation_losses == 2
        assert tsr.overtime_wins == 2
        assert tsr.overtime_losses == 2
        assert tsr.shootout_wins == 2
        assert tsr.shootout_losses == 2
        assert tsr.wins == 7
        assert tsr.losses == 6
        assert tsr.ties == 2
        assert tsr.points == 14 + 2 + 2 + 2
        assert tsr.goals_for == 69
        assert tsr.goals_against == 25
        assert tsr.goal_differential == 44
        assert tsr.record == '7-6-2'

    def test_point_percentage(self, team_season_registration_factory, season_2024, season_2023, corlears_hookers,
                              division4):
        # No games played
        assert team_season_registration_factory(
            season=season_2024,
            team=corlears_hookers,
            division=division4,
            home_games_played=0,
            away_games_played=0,
            home_regulation_wins=0,
            home_regulation_losses=0,
            home_overtime_wins=0,
            home_overtime_losses=0,
            home_shootout_wins=0,
            home_shootout_losses=0,
            home_ties=0,
            away_regulation_wins=0,
            away_regulation_losses=0,
            away_overtime_wins=0,
            away_overtime_losses=0,
            away_shootout_wins=0,
            away_shootout_losses=0,
            away_ties=0,
            home_goals_for=0,
            home_goals_against=0,
            away_goals_for=0,
            away_goals_against=0,
        ).point_percentage is None

        # Games played
        assert team_season_registration_factory(
            season=season_2023,
            team=corlears_hookers,
            division=division4,
            home_games_played=7,
            away_games_played=8,
            home_regulation_wins=1,
            home_regulation_losses=1,
            home_overtime_wins=1,
            home_overtime_losses=1,
            home_shootout_wins=1,
            home_shootout_losses=1,
            home_ties=1,
            away_regulation_wins=2,
            away_regulation_losses=1,
            away_overtime_wins=1,
            away_overtime_losses=1,
            away_shootout_wins=1,
            away_shootout_losses=1,
            away_ties=1,
            home_goals_for=35,
            home_goals_against=10,
            away_goals_for=34,
            away_goals_against=15,
        ).point_percentage == 0.667

    def test_to_str(self, corlears_hookers_2024_season_registration):
        assert str(corlears_hookers_2024_season_registration) == ('Corlears Hookers - Division 4 - 03/31/2024 - '
                                                                  '10/31/2024 Season')

    def test_season_team_uniq(self, team_season_registration_factory, corlears_hookers_2024_season_registration,
                              division2):
        with pytest.raises(ValidationError) as e:
            team_season_registration_factory(
                season=corlears_hookers_2024_season_registration.season,
                team=corlears_hookers_2024_season_registration.team,
                division=division2,
                home_games_played=7,
                away_games_played=8,
                home_regulation_wins=1,
                home_regulation_losses=1,
                home_overtime_wins=1,
                home_overtime_losses=1,
                home_shootout_wins=1,
                home_shootout_losses=1,
                home_ties=1,
                away_regulation_wins=2,
                away_regulation_losses=1,
                away_overtime_wins=1,
                away_overtime_losses=1,
                away_shootout_wins=1,
                away_shootout_losses=1,
                away_ties=1,
                home_goals_for=35,
                home_goals_against=10,
                away_goals_for=34,
                away_goals_against=15,
            )
        assert e.value.message_dict == {
            '__all__': ['Team season registration with this Season and Team already exists.']
        }
