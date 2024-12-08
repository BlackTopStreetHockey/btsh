import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F

from api.utils.datetime import format_datetime
from common.models import BaseModel
from games.managers import GameManager, GameQuerySet
from teams.models import Team


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

        season = getattr(self, 'season', None)

        if self.day and season and (season.start > self.day or season.end < self.day):
            raise ValidationError({
                'day': f'Day must be between {season.start_formatted} and {season.end_formatted}.'
            })

    def __str__(self):
        return format_datetime(self.day)


class GameResultsEnum(models.TextChoices):
    FINAL = 'final', 'Final'
    FINAL_OT = 'final_ot', 'Final/OT'
    FINAL_SO = 'final_so', 'Final/SO'


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

    SCHEDULED = 'scheduled'
    CANCELLED = 'cancelled'
    COMPLETED = 'completed'
    STATUSES = {
        SCHEDULED: 'Scheduled',
        CANCELLED: 'Cancelled',
        COMPLETED: 'Completed',
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
    status = models.CharField(max_length=16, choices=STATUSES, default=SCHEDULED)

    objects = GameManager.from_queryset(GameQuerySet)()

    def _get_team_display(self, team: Team, num_goals: int):
        if self.status != Game.COMPLETED:
            return team.name

        win_loss_tie = None
        if self.winning_team_id == team.id:
            win_loss_tie = 'W'
        elif self.losing_team_id == team.id:
            win_loss_tie = 'L'
        elif self.winning_team_id is None and self.losing_team_id is None:
            win_loss_tie = 'T'

        team_display = f'{team.name} ({num_goals})'
        return f'{team_display} - {win_loss_tie}' if win_loss_tie else team_display

    @property
    def teams(self):
        return [self.home_team, self.away_team]

    @property
    def home_team_display(self):
        return self._get_team_display(self.home_team, self.home_team_num_goals)

    @property
    def away_team_display(self):
        return self._get_team_display(self.away_team, self.away_team_num_goals)

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

        team = getattr(self, 'team', None)
        game = getattr(self, 'game', None)

        if team and game and team not in game.teams:
            team_names = ' or '.join([t.name for t in game.teams])
            raise ValidationError({'team': f'Team must be {team_names}.'})

    def __str__(self):
        return f'{self.user.get_full_name()} - {self.team} - {self.game}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('game', 'user', 'team'), name='game_user_team_uniq')
        ]


class GameGoal(BaseModel):
    """Goals for the game"""
    FIRST = '1'
    SECOND = '2'
    OT = 'ot'
    SO = 'so'
    PERIODS = {
        FIRST: '1st',
        SECOND: '2nd',
        OT: 'OT',
        SO: 'SO',
    }

    game = models.ForeignKey(Game, on_delete=models.PROTECT, related_name='goals')
    team = models.ForeignKey('teams.Team', on_delete=models.PROTECT, related_name='goals')
    period = models.CharField(max_length=4, choices=PERIODS)
    scored_by = models.ForeignKey(GamePlayer, on_delete=models.PROTECT, related_name='goals')
    assisted_by1 = models.ForeignKey(
        GamePlayer,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='primary_assists',
    )
    assisted_by2 = models.ForeignKey(
        GamePlayer,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='secondary_assists',
    )

    def _validate_game_player(self, game_player: GamePlayer, game: Game, team: Team):
        """Validates the selected game player belongs to the selected team and game."""
        errors = []

        if game_player and game and game_player.game_id != game.id:
            errors.append('This player does not belong to the selected game.')

        if game_player and team and game_player.team_id != team.id:
            errors.append('This player does not belong to the selected team.')

        return errors

    def _validate_game_players(self, gp1: GamePlayer, gp2: GamePlayer):
        """Validates the selected game players are not the same, i.e. the scorer isn't given an assist."""
        errors = []

        if gp1 and gp2 and gp1.id == gp2.id:
            errors.append('This player can\'t be selected more than once.')

        return errors

    def clean(self):
        super().clean()
        errors = {}

        team = getattr(self, 'team', None)
        game = getattr(self, 'game', None)
        scored_by = getattr(self, 'scored_by', None)
        assisted_by1 = getattr(self, 'assisted_by1', None)
        assisted_by2 = getattr(self, 'assisted_by2', None)

        if team and game and team not in game.teams:
            team_names = ' or '.join([t.name for t in game.teams])
            errors.setdefault('team', []).append(f'Team must be {team_names}.')

        # Ensure game player belongs to the game and team
        if errors1 := self._validate_game_player(scored_by, game, team):
            errors.setdefault('scored_by', []).extend(errors1)
        if errors2 := self._validate_game_player(assisted_by1, game, team):
            errors.setdefault('assisted_by1', []).extend(errors2)
        if errors3 := self._validate_game_player(assisted_by2, game, team):
            errors.setdefault('assisted_by2', []).extend(errors3)

        # Ensure scorer, assist1, assist2 are all different
        if errors4 := self._validate_game_players(scored_by, assisted_by1):
            errors.setdefault('assisted_by1', []).extend(errors4)
        if errors5 := self._validate_game_players(scored_by, assisted_by2):
            errors.setdefault('assisted_by2', []).extend(errors5)
        if errors6 := self._validate_game_players(assisted_by1, assisted_by2):
            errors.setdefault('assisted_by2', []).extend(errors6)

        if not assisted_by1 and assisted_by2:
            errors.setdefault('assisted_by1', []).append('This field is required when a secondary assist is provided.')

        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return f'{self.scored_by.user.get_full_name()} - {self.team} - {self.game}'
