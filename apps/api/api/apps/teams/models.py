from django.contrib.postgres.fields import ArrayField
from django.db import models

from common.models import BaseModel


class Team(BaseModel):
    name = models.CharField(max_length=64, unique=True)
    short_name = models.CharField(max_length=8, unique=True)
    logo = models.ImageField(upload_to='teams/logos/')
    jersey_colors = ArrayField(
        base_field=models.CharField(max_length=32),
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
