import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F

from api.utils.datetime import format_datetime
from common.models import BaseModel


def default_game_duration():
    return datetime.timedelta(minutes=50)


class GameDay(BaseModel):
    """A day in which games take place, this will almost always be sundays"""
    day = models.DateField(unique=True)
    season = models.ForeignKey('seasons.Season', on_delete=models.PROTECT)
    opening_team = models.ForeignKey('teams.Team', on_delete=models.PROTECT, related_name='opening_team_game_days')
    closing_team = models.ForeignKey('teams.Team', on_delete=models.PROTECT, related_name='closing_team_game_days')

    def clean(self):
        super().clean()

        if self.day and self.season and (self.season.start > self.day or self.season.end < self.day):
            raise ValidationError({
                'day': f'Day must be between {self.season.start_formatted} and {self.season.end_formatted}.'
            })

    def __str__(self):
        return format_datetime(self.day)


class Game(BaseModel):
    EAST = 'east'
    WEST = 'west'
    COURTS = {
        EAST: 'East',
        WEST: 'West',
    }

    REGULAR = 'regular'
    PLAYOFF = 'playoff'
    TYPES = {
        REGULAR: 'Regular',
        PLAYOFF: 'Playoff',
    }

    game_day = models.ForeignKey(GameDay, on_delete=models.PROTECT, related_name='games')
    start = models.TimeField()
    duration = models.DurationField(default=default_game_duration)
    end = models.GeneratedField(
        expression=F('start') + F('duration'),
        output_field=models.TimeField(),
        db_persist=True
    )
    home_team = models.ForeignKey('teams.Team', on_delete=models.PROTECT, related_name='home_team_games')
    away_team = models.ForeignKey('teams.Team', on_delete=models.PROTECT, related_name='away_team_games')
    location = models.CharField(max_length=256, default='Tompkins Square Park')
    court = models.CharField(max_length=8, choices=COURTS)
    type = models.CharField(max_length=8, choices=TYPES, default=REGULAR)

    @property
    def teams(self):
        return [self.home_team, self.away_team]

    def __str__(self):
        return f'{self.game_day} {self.start.strftime("%I:%M%p")} {self.home_team.name} vs. {self.away_team.name}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('game_day', 'start', 'home_team', 'away_team'), name='game_uniq')
        ]


class GameReferee(BaseModel):
    """Referees for the game"""
    STRING = 'string'
    FENCE = 'fence'
    TYPES = {
        STRING: 'String',
        FENCE: 'Fence',
    }

    game = models.ForeignKey(Game, on_delete=models.PROTECT, related_name='referees')
    user = models.ForeignKey('users.User', on_delete=models.PROTECT, related_name='game_referees')
    type = models.CharField(max_length=8, choices=TYPES)

    def __str__(self):
        return f'{self.user.get_full_name()} - {self.game}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('game', 'user', 'type'), name='game_user_type_uniq')
        ]


class GamePlayer(BaseModel):
    """Players for the game"""
    game = models.ForeignKey(Game, on_delete=models.PROTECT, related_name='players')
    user = models.ForeignKey('users.User', on_delete=models.PROTECT, related_name='game_players')
    team = models.ForeignKey('teams.Team', on_delete=models.PROTECT, related_name='game_players')
    is_substitute = models.BooleanField(default=False)
    is_goalie = models.BooleanField()

    def clean(self):
        super().clean()

        if self.team and self.game and self.team not in self.game.teams:
            team_names = ' or '.join([t.name for t in self.game.teams])
            raise ValidationError({'team': f'Team must be {team_names}.'})

    def __str__(self):
        return f'{self.user.get_full_name()} - {self.game}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('game', 'user', 'team'), name='game_user_team_uniq')
        ]


class GameGoal(BaseModel):
    game = models.ForeignKey(Game, on_delete=models.PROTECT, related_name='goals')
    team = models.ForeignKey('teams.Team', on_delete=models.PROTECT, related_name='goals')
    scorer = models.ForeignKey(GamePlayer, on_delete=models.PROTECT, related_name='goals')
    assist1 = models.ForeignKey(
        GamePlayer,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='primary_assists',
    )
    assist2 = models.ForeignKey(
        GamePlayer,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='secondary_assists',
    )

    def clean(self):
        super().clean()
        errors = []

        if self.game and self.team and self.team not in self.game.teams:
            errors.append({'team': 'Team must be either the home or away team.'})

        if self.scorer and self.assist1:
            ...

        if self.scorer and self.assist2:
            ...

        if self.assist1 and self.assist2:
            ...

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return f'{self.scorer.get_full_name()} - {self.team} - {self.game}'
