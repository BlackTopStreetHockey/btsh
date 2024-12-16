from django.contrib.postgres.fields import ArrayField
from django.db import models

from common.models import BaseModel


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
    season = models.ForeignKey('seasons.Season', on_delete=models.PROTECT, related_name='team_registrations')
    team = models.ForeignKey('teams.Team', on_delete=models.PROTECT, related_name='team_season_registrations')
    division = models.ForeignKey(
        'divisions.Division', on_delete=models.PROTECT, related_name='division_season_registrations'
    )

    def __str__(self):
        return f'{self.team} - {self.division} - {self.season}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('season', 'team'), name='season_team_uniq')
        ]
