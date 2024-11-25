from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from api.utils.datetime import format_datetime
from common.models import BaseModel


class Season(BaseModel):
    start = models.DateField()
    end = models.DateField()

    @property
    def start_formatted(self):
        return format_datetime(self.start)

    @property
    def end_formatted(self):
        return format_datetime(self.end)

    @property
    def is_past(self):
        return timezone.now().date() > self.end

    @property
    def is_current(self):
        return self.start <= timezone.now().date() <= self.end

    @property
    def is_future(self):
        return timezone.now().date() < self.start

    @property
    def year(self):
        return self.start.year

    def clean(self):
        super().clean()
        if self.start and self.end and self.end <= self.start:
            raise ValidationError({
                'start': 'Start date must be before end date.',
                'end': 'End date must be after start date.'
            })

    def __str__(self):
        return f'{self.start_formatted} - {self.end_formatted} Season'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('start', 'end'), name='start_end_uniq')
        ]


class SeasonRegistration(BaseModel):
    DEFENSE = 'defense'
    FORWARD = 'forward'
    GOALIE = 'goalie'
    POSITIONS = {
        DEFENSE: 'Defense',
        FORWARD: 'Forward',
        GOALIE: 'Goalie',
    }

    BROOKLYN = 'brooklyn'
    BRONX = 'bronx'
    MANHATTAN = 'manhattan'
    QUEENS = 'queens'
    LONG_ISLAND = 'long_island'
    NEW_JERSEY = 'new_jersey'
    CONNECTICUT = 'connecticut'
    WESTCHESTER = 'westchester'
    LOCATIONS = {
        BROOKLYN: 'Brooklyn',
        BRONX: 'Bronx',
        MANHATTAN: 'Manhattan',
        QUEENS: 'Queens',
        LONG_ISLAND: 'Long Island',
        NEW_JERSEY: 'New Jersey',
        CONNECTICUT: 'Connecticut',
        WESTCHESTER: 'Westchester',
    }

    user = models.ForeignKey('users.User', on_delete=models.PROTECT, related_name='season_registrations')
    season = models.ForeignKey('seasons.Season', on_delete=models.PROTECT, related_name='user_team_registrations')
    team = models.ForeignKey('teams.Team', on_delete=models.PROTECT, related_name='user_season_registrations')
    is_captain = models.BooleanField()
    position = models.CharField(max_length=16, choices=POSITIONS)
    # We'll keep created_at as an internal field, this field will default to approx the same value as created_at but can
    # be overridden if we'd like
    registered_at = models.DateTimeField(default=timezone.now)
    signature = models.CharField(max_length=512)
    location = models.CharField(max_length=16, choices=LOCATIONS)
    interested_in = models.TextField(null=True, blank=True)
    mid_season_party_ideas = models.TextField(null=True, blank=True)

    def clean(self):
        super().clean()

        user = getattr(self, 'user', None)
        signature = getattr(self, 'signature', None)

        if user and signature and user.get_full_name() != signature:
            raise ValidationError({'signature': 'Signature must match the user\'s full name.'})

    def __str__(self):
        return f'{self.user} - {self.season} - {self.team}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('user', 'season', 'team'), name='user_season_team_uniq')
        ]
