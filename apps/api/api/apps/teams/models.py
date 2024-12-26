from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import F, Value
from django.db.models.functions import Cast, Concat

from common.models import BaseModel
from .managers import TeamSeasonRegistrationManager, TeamSeasonRegistrationQuerySet


class Team(BaseModel):
    name = models.CharField(max_length=64, unique=True)
    short_name = models.CharField(max_length=10, unique=True)
    logo = models.ImageField(upload_to='teams/logos/')
    jersey_colors = ArrayField(
        base_field=models.CharField(max_length=32),
        null=True,
        blank=True,
        help_text='Comma separated list of jersey colors.'
    )

    def __str__(self):
        return self.name


class TeamSeasonRegistration(BaseModel):
    """Stores a team's registration for a particular season, including additional metadata such as their division"""
    BASE_FIELDS = (
        # Totals
        'points', 'wins', 'losses', 'ties', 'record',
        'overtime_losses', 'shootout_losses',
        'games_played',
        'goals_for', 'goals_against', 'goal_differential',
        'home_wins', 'home_losses',
        'away_wins', 'away_losses',
        'regulation_wins', 'regulation_losses',
        'overtime_wins', 'shootout_wins',
        # Games played
        'home_games_played', 'away_games_played',
        # Home wins, losses, ties
        'home_regulation_wins', 'home_regulation_losses',
        'home_overtime_wins', 'home_overtime_losses',
        'home_shootout_wins', 'home_shootout_losses',
        'home_ties',
        # Away wins, losses, ties
        'away_regulation_wins', 'away_regulation_losses',
        'away_overtime_wins', 'away_overtime_losses',
        'away_shootout_wins', 'away_shootout_losses',
        'away_ties',
        # Goals
        'home_goals_for', 'home_goals_against',
        'away_goals_for', 'away_goals_against',
    )
    FIELDS = (
        'team', 'season', 'division',
        *BASE_FIELDS,
    )
    HOME_WINS_EXPRESSION = F('home_regulation_wins') + F('home_overtime_wins') + F('home_shootout_wins')
    AWAY_WINS_EXPRESSION = F('away_regulation_wins') + F('away_overtime_wins') + F('away_shootout_wins')
    WINS_EXPRESSION = HOME_WINS_EXPRESSION + AWAY_WINS_EXPRESSION
    REGULATION_WINS_EXPRESSION = F('home_regulation_wins') + F('away_regulation_wins')
    OVERTIME_WINS_EXPRESSION = F('home_overtime_wins') + F('away_overtime_wins')
    SHOOTOUT_WINS_EXPRESSION = F('home_shootout_wins') + F('away_shootout_wins')

    HOME_LOSSES_EXPRESSION = F('home_regulation_losses') + F('home_overtime_losses') + F('home_shootout_losses')
    AWAY_LOSSES_EXPRESSION = F('away_regulation_losses') + F('away_overtime_losses') + F('away_shootout_losses')
    LOSSES_EXPRESSION = HOME_LOSSES_EXPRESSION + AWAY_LOSSES_EXPRESSION
    REGULATION_LOSSES_EXPRESSION = F('home_regulation_losses') + F('away_regulation_losses')
    OVERTIME_LOSSES_EXPRESSION = F('home_overtime_losses') + F('away_overtime_losses')
    SHOOTOUT_LOSSES_EXPRESSION = F('home_shootout_losses') + F('away_shootout_losses')

    TIES_EXPRESSION = F('home_ties') + F('away_ties')

    HOME_GOALS_FOR_EXPRESSION = F('home_goals_for')
    AWAY_GOALS_FOR_EXPRESSION = F('away_goals_for')
    GOALS_FOR_EXPRESSION = HOME_GOALS_FOR_EXPRESSION + AWAY_GOALS_FOR_EXPRESSION
    HOME_GOALS_AGAINST_EXPRESSION = F('home_goals_against')
    AWAY_GOALS_AGAINST_EXPRESSION = F('away_goals_against')
    GOALS_AGAINST_EXPRESSION = HOME_GOALS_AGAINST_EXPRESSION + AWAY_GOALS_AGAINST_EXPRESSION

    WIN_POINT_VALUE = 2
    OTL_SOL_POINT_VALUE = 1
    TIE_POINT_VALUE = 1

    season = models.ForeignKey('seasons.Season', on_delete=models.PROTECT, related_name='team_registrations')
    team = models.ForeignKey('teams.Team', on_delete=models.PROTECT, related_name='team_season_registrations')
    division = models.ForeignKey(
        'divisions.Division', on_delete=models.PROTECT, related_name='division_season_registrations'
    )
    # Games played
    home_games_played = models.PositiveSmallIntegerField(default=0)
    away_games_played = models.PositiveSmallIntegerField(default=0)

    # Home wins, losses, ties
    home_regulation_wins = models.PositiveSmallIntegerField(default=0)
    home_regulation_losses = models.PositiveSmallIntegerField(default=0)
    home_overtime_wins = models.PositiveSmallIntegerField(default=0)
    home_overtime_losses = models.PositiveSmallIntegerField(default=0)
    home_shootout_wins = models.PositiveSmallIntegerField(default=0)
    home_shootout_losses = models.PositiveSmallIntegerField(default=0)
    home_ties = models.PositiveSmallIntegerField(default=0)

    # Away wins, losses, ties
    away_regulation_wins = models.PositiveSmallIntegerField(default=0)
    away_regulation_losses = models.PositiveSmallIntegerField(default=0)
    away_overtime_wins = models.PositiveSmallIntegerField(default=0)
    away_overtime_losses = models.PositiveSmallIntegerField(default=0)
    away_shootout_wins = models.PositiveSmallIntegerField(default=0)
    away_shootout_losses = models.PositiveSmallIntegerField(default=0)
    away_ties = models.PositiveSmallIntegerField(default=0)

    # Goals
    home_goals_for = models.PositiveSmallIntegerField(default=0)
    home_goals_against = models.PositiveSmallIntegerField(default=0)
    away_goals_for = models.PositiveSmallIntegerField(default=0)
    away_goals_against = models.PositiveSmallIntegerField(default=0)

    # Totals
    games_played = models.GeneratedField(
        expression=F('home_games_played') + F('away_games_played'),
        output_field=models.PositiveSmallIntegerField(),
        db_persist=True,
    )
    home_wins = models.GeneratedField(
        expression=HOME_WINS_EXPRESSION,
        output_field=models.PositiveSmallIntegerField(),
        db_persist=True,
    )
    home_losses = models.GeneratedField(
        expression=HOME_LOSSES_EXPRESSION,
        output_field=models.PositiveSmallIntegerField(),
        db_persist=True,
    )
    away_wins = models.GeneratedField(
        expression=AWAY_WINS_EXPRESSION,
        output_field=models.PositiveSmallIntegerField(),
        db_persist=True,
    )
    away_losses = models.GeneratedField(
        expression=AWAY_LOSSES_EXPRESSION,
        output_field=models.PositiveSmallIntegerField(),
        db_persist=True,
    )
    regulation_wins = models.GeneratedField(
        expression=REGULATION_WINS_EXPRESSION,
        output_field=models.PositiveSmallIntegerField(),
        db_persist=True,
    )
    regulation_losses = models.GeneratedField(
        expression=REGULATION_LOSSES_EXPRESSION,
        output_field=models.PositiveSmallIntegerField(),
        db_persist=True,
    )
    overtime_wins = models.GeneratedField(
        expression=OVERTIME_WINS_EXPRESSION,
        output_field=models.PositiveSmallIntegerField(),
        db_persist=True,
    )
    overtime_losses = models.GeneratedField(
        expression=OVERTIME_LOSSES_EXPRESSION,
        output_field=models.PositiveSmallIntegerField(),
        db_persist=True,
    )
    shootout_wins = models.GeneratedField(
        expression=SHOOTOUT_WINS_EXPRESSION,
        output_field=models.PositiveSmallIntegerField(),
        db_persist=True,
    )
    shootout_losses = models.GeneratedField(
        expression=SHOOTOUT_LOSSES_EXPRESSION,
        output_field=models.PositiveSmallIntegerField(),
        db_persist=True,
    )
    wins = models.GeneratedField(
        expression=WINS_EXPRESSION,
        output_field=models.PositiveSmallIntegerField(),
        db_persist=True,
    )
    losses = models.GeneratedField(
        expression=LOSSES_EXPRESSION,
        output_field=models.PositiveSmallIntegerField(),
        db_persist=True,
    )
    ties = models.GeneratedField(
        expression=TIES_EXPRESSION,
        output_field=models.PositiveSmallIntegerField(),
        db_persist=True,
    )

    points = models.GeneratedField(
        expression=(
            (WINS_EXPRESSION * WIN_POINT_VALUE) +
            (OVERTIME_LOSSES_EXPRESSION * OTL_SOL_POINT_VALUE) +
            (SHOOTOUT_LOSSES_EXPRESSION * OTL_SOL_POINT_VALUE) +
            (TIES_EXPRESSION * TIE_POINT_VALUE)
        ),
        output_field=models.PositiveSmallIntegerField(),
        db_persist=True,
    )

    goals_for = models.GeneratedField(
        expression=GOALS_FOR_EXPRESSION,
        output_field=models.PositiveSmallIntegerField(),
        db_persist=True,
    )
    goals_against = models.GeneratedField(
        expression=GOALS_AGAINST_EXPRESSION,
        output_field=models.PositiveSmallIntegerField(),
        db_persist=True,
    )
    goal_differential = models.GeneratedField(
        expression=GOALS_FOR_EXPRESSION - GOALS_AGAINST_EXPRESSION,
        output_field=models.PositiveSmallIntegerField(),
        db_persist=True,
    )
    record = models.GeneratedField(
        expression=Concat(
            Cast(WINS_EXPRESSION, output_field=models.CharField()),
            Value('-'),
            Cast(LOSSES_EXPRESSION, output_field=models.CharField()),
            Value('-'),
            Cast(TIES_EXPRESSION, output_field=models.CharField()),
        ),
        output_field=models.CharField(),
        db_persist=True,
    )

    objects = TeamSeasonRegistrationManager.from_queryset(TeamSeasonRegistrationQuerySet)()

    def __str__(self):
        return f'{self.team} - {self.division} - {self.season}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('season', 'team'), name='season_team_uniq')
        ]
