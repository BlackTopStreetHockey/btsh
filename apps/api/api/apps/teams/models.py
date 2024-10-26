from django.contrib.postgres.fields import ArrayField
from django.db import models

from common.models import BaseModel


class Team(BaseModel):
    name = models.CharField(max_length=64, unique=True)
    logo = models.ImageField(upload_to='teams/logos/')
    jersey_colors = ArrayField(
        base_field=models.CharField(max_length=32),
        null=True,
        blank=True,
        help_text='Comma separated list of jersey colors.'
    )

    def __str__(self):
        return self.name
