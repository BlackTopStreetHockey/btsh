from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from common.models import BaseModel
from users.managers import UserSeasonRegistrationManager, UserSeasonRegistrationQuerySet


class User(AbstractUser):
    MALE = 'male'
    FEMALE = 'female'
    NON_BINARY = 'non_binary'
    GENDERS = {
        MALE: 'Male',
        FEMALE: 'Female',
        NON_BINARY: 'Non-binary',
    }

    gender = models.CharField(max_length=16, choices=GENDERS, null=True, blank=True)

    def __str__(self):
        return f'{self.get_full_name()} - {self.get_username()}'


class UserSeasonRegistration(BaseModel):
    """Stores a user's registration for a particular season, including additional metadata such as their team"""
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

    objects = UserSeasonRegistrationManager.from_queryset(UserSeasonRegistrationQuerySet)()

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
