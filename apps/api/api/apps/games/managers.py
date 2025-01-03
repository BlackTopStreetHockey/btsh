from django.db import models
from django.db.models import Case, Count, F, OuterRef, Q, Subquery, Sum, Value, When

from teams.models import TeamSeasonRegistration


class GameQuerySet(models.QuerySet):
    def with_scores(self):
        from games.models import GameGoal, GameResultsEnum, Game

        return self.annotate(
            home_team_num_goals=Case(
                When(status=Game.COMPLETED, then=Count('goals', filter=Q(goals__team=F('home_team')))),
                default=None,
            ),
            away_team_num_goals=Case(
                When(status=Game.COMPLETED, then=Count('goals', filter=Q(goals__team=F('away_team')))),
                default=None,
            ),
            winning_team_id=Case(
                When(home_team_num_goals__gt=F('away_team_num_goals'), then=F('home_team')),
                When(home_team_num_goals__lt=F('away_team_num_goals'), then=F('away_team')),
                When(home_team_num_goals=F('away_team_num_goals'), then=None),  # Tie or game not completed
            ),
            losing_team_id=Case(
                When(winning_team_id=F('home_team'), then=F('away_team')),
                When(winning_team_id=F('away_team'), then=F('home_team')),
                When(winning_team_id=None, then=None),  # Tie or game not completed
            ),

            # TODO tweak this if changing how we handle shootouts, currently if a game has a goal with period "SO" it's
            # treated as Final/SO
            num_shootout_goals=Count('goals', filter=Q(goals__period=GameGoal.SO)),
            num_ot_goals=Count('goals', filter=Q(goals__period=GameGoal.OT)),
            result=Case(
                When(~Q(status=Game.COMPLETED), then=None),
                When(num_shootout_goals__gt=0, then=Value(GameResultsEnum.FINAL_SO.value)),
                When(num_ot_goals__gt=0, then=Value(GameResultsEnum.FINAL_OT.value)),
                default=Value(GameResultsEnum.FINAL.value),
            ),
            get_result_display=Case(
                When(result=None, then=None),
                When(result=GameResultsEnum.FINAL_SO.value, then=Value(GameResultsEnum.FINAL_SO.label)),
                When(result=GameResultsEnum.FINAL_OT.value, then=Value(GameResultsEnum.FINAL_OT.label)),
                default=Value(GameResultsEnum.FINAL.label),
            )
        )

    def with_team_divisions(self):
        season_registrations = TeamSeasonRegistration.objects.filter(season=OuterRef('game_day__season'))
        home_team_season_registrations = season_registrations.filter(team=OuterRef('home_team'))
        away_team_season_registrations = season_registrations.filter(team=OuterRef('away_team'))

        return self.annotate(
            home_team_division_id=Subquery(home_team_season_registrations.values('division_id')),
            home_team_division_name=Subquery(home_team_season_registrations.values('division__name')),

            away_team_division_id=Subquery(away_team_season_registrations.values('division_id')),
            away_team_division_name=Subquery(away_team_season_registrations.values('division__name')),
        )

    def for_team(self, team):
        return self.filter(Q(home_team=team) | Q(away_team=team))

    def for_stats(self, team, season, game_type):
        """Get the games to be used to compute stats for the given team in the given season."""
        from games.models import GameGoal

        home_team_filter = Q(home_team=team)
        away_team_filter = Q(away_team=team)
        goals_for_filter = Q(goals__team=team)
        goals_against_filter = Q(goals__team_against=team)
        not_shootout_goal_filter = ~Q(goals__period=GameGoal.SO)

        return self.for_team(team).filter(
            status=self.model.COMPLETED,
            type=game_type,
            game_day__season=season,
        ).select_related(
            'home_team',
            'away_team',
            'game_day__season',
        ).prefetch_related(
            'goals__team',
            'goals__team_against',
        ).with_scores().annotate(
            _home_goals_for=Count('goals', filter=home_team_filter & goals_for_filter & not_shootout_goal_filter),
            _home_goals_against=Count(
                'goals',
                filter=home_team_filter & goals_against_filter & not_shootout_goal_filter
            ),
            _away_goals_for=Count('goals', filter=away_team_filter & goals_for_filter & not_shootout_goal_filter),
            _away_goals_against=Count(
                'goals',
                filter=away_team_filter & goals_against_filter & not_shootout_goal_filter
            ),
        )


class GameManager(models.Manager):
    def with_stats(self, team, season, game_type) -> dict:
        from games.models import GameResultsEnum

        regulation_filter = Q(result=GameResultsEnum.FINAL)
        overtime_filter = Q(result=GameResultsEnum.FINAL_OT)
        shootout_filter = Q(result=GameResultsEnum.FINAL_SO)
        home_team_filter = Q(home_team=team)
        away_team_filter = Q(away_team=team)
        winning_team_filter = Q(winning_team_id=team.id)
        losing_team_filter = Q(losing_team_id=team.id)
        tie_filter = Q(winning_team_id=None) & Q(losing_team_id=None)

        return self.for_stats(
            team, season, game_type
        ).aggregate(
            # Games played
            home_games_played=Count('id', filter=home_team_filter),
            away_games_played=Count('id', filter=away_team_filter),

            # Home wins, losses, ties
            home_regulation_wins=Count('id', filter=home_team_filter & regulation_filter & winning_team_filter),
            home_regulation_losses=Count('id', filter=home_team_filter & regulation_filter & losing_team_filter),
            home_overtime_wins=Count('id', filter=home_team_filter & overtime_filter & winning_team_filter),
            home_overtime_losses=Count('id', filter=home_team_filter & overtime_filter & losing_team_filter),
            home_shootout_wins=Count('id', filter=home_team_filter & shootout_filter & winning_team_filter),
            home_shootout_losses=Count('id', filter=home_team_filter & shootout_filter & losing_team_filter),
            home_ties=Count('id', filter=home_team_filter & tie_filter),

            # Away wins, losses, ties
            away_regulation_wins=Count('id', filter=away_team_filter & regulation_filter & winning_team_filter),
            away_regulation_losses=Count('id', filter=away_team_filter & regulation_filter & losing_team_filter),
            away_overtime_wins=Count('id', filter=away_team_filter & overtime_filter & winning_team_filter),
            away_overtime_losses=Count('id', filter=away_team_filter & overtime_filter & losing_team_filter),
            away_shootout_wins=Count('id', filter=away_team_filter & shootout_filter & winning_team_filter),
            away_shootout_losses=Count('id', filter=away_team_filter & shootout_filter & losing_team_filter),
            away_ties=Count('id', filter=away_team_filter & tie_filter),

            # Goals
            home_goals_for=Sum(F('_home_goals_for'), default=0),
            home_goals_against=Sum(F('_home_goals_against'), default=0),
            away_goals_for=Sum(F('_away_goals_for'), default=0),
            away_goals_against=Sum(F('_away_goals_against'), default=0),
        )
