from django.db import models
from django.db.models import Count, F, Q, Window
from django.db.models.functions import RowNumber

from games.models import Game, GameGoal


class UserSeasonRegistrationQuerySet(models.QuerySet):
    def for_team(self, team, season=None):
        kwargs = {'team': team}
        if season:
            kwargs.update({'season': season})
        return self.filter(**kwargs).select_related('user', 'team', 'season')

    def with_stats(self, game_type):
        """
        Computes a user's stats for the provided game type (regular, playoff), team and season. The team and season are
        taken from the user season registration.
        """
        season_filter = Q(user__game_players__game__game_day__season=F('season'))
        team_filter = Q(user__game_players__team=F('team'))
        completed_game_filter = Q(user__game_players__game__status=Game.COMPLETED)
        game_type_filter = Q(user__game_players__game__type=game_type)
        not_shootout_goal_filter = ~Q(user__game_players__goals__period=GameGoal.SO)

        return self.annotate(
            games_played=Count(
                'user__game_players',
                distinct=True,
                filter=season_filter & team_filter & completed_game_filter & game_type_filter,
            ),
            goals=Count(
                'user__game_players__goals',
                distinct=True,
                filter=(
                    season_filter & team_filter & completed_game_filter & game_type_filter & not_shootout_goal_filter
                ),
            ),
            primary_assists=Count(
                'user__game_players__primary_assists',
                distinct=True,
                filter=season_filter & team_filter & completed_game_filter & game_type_filter,
            ),
            secondary_assists=Count(
                'user__game_players__secondary_assists',
                distinct=True,
                filter=season_filter & team_filter & completed_game_filter & game_type_filter,
            ),
            assists=F('primary_assists') + F('secondary_assists'),
            points=F('goals') + F('assists'),
        )

    def with_place_by_team_and_season(self, game_type):
        """Computes a user's placing/ranking for the provided game type, registered team, registered season."""
        return self.with_stats(game_type).annotate(
            place=Window(
                expression=RowNumber(),
                partition_by=[F('team'), F('season')],
                order_by=[
                    F('points').desc(),
                ]
            )
        )


class UserSeasonRegistrationManager(models.Manager):
    ...
