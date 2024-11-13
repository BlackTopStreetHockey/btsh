from django.contrib.postgres.fields import ArrayField
from django.db import models

from common.models import BaseModel


class Team(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    short_name = models.CharField(max_length=10, unique=True)
    logo = models.ImageField(upload_to='team_logos/')
    jersey_colors = ArrayField(models.CharField(max_length=50), size=2, null=True, blank=True, help_text='Comma separated list of jersey colors')
    established = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text='Year the team was established'
    )
    description = models.TextField(
        null=True,
        blank=True,
        help_text='Team description including championship years'
    )
    instagram_url = models.URLField(
        max_length=200,
        null=True,
        blank=True,
        help_text='Team Instagram profile URL'
    )

    def __str__(self):
        return self.name
