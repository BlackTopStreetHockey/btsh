import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F

from common.models import BaseModel
from api.utils.datetime import format_datetime


"""
Questions/Ideas:

Can a game day have many opening and closing teams? If so would need a M2M relationship over FK

We could store the full date + time on the game instead of date on game day and time on game but I think this would
be more annoying for maintenance (changing game datese for rainout, etc).

How to handle teams changing divisions, store home team division and away team division on game?

"""


def default_game_duration():
    return datetime.timedelta(minutes=50)


class GameDay(BaseModel):
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
    # Dict keys are what get stored in the db, dict values are what's displayed to end users
    COURTS = {
        EAST: 'East',
        WEST: 'West',
    }

    game_day = models.ForeignKey(GameDay, on_delete=models.PROTECT)
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

    def __str__(self):
        return f'{self.game_day} {self.start.strftime("%I:%M%p")} {self.home_team.name} vs. {self.away_team.name}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('game_day', 'start', 'home_team', 'away_team'), name='game_uniq')
        ]
