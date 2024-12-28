import uuid
from pathlib import Path
from urllib.parse import urlparse

import requests
from django import forms
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.validators import URLValidator
from django.db import models
from import_export import fields, resources, widgets
from requests.exceptions import RequestException

from divisions.models import Division
from games.models import GameDay, GamePlayer
from seasons.models import Season
from teams.models import Team
from users.models import User


class EmailWidget(widgets.CharWidget):
    def clean(self, value, row=None, **kwargs):
        val = super().clean(value, row, **kwargs)
        if val:
            return forms.EmailField().clean(val).lower()
        return val


class ImageWidget(widgets.CharWidget):
    def clean(self, value, row=None, **kwargs):
        val = super().clean(value, row, **kwargs)
        if val:
            # Validate it's a well-formed url we can download from
            try:
                URLValidator(schemes=['http', 'https'])(val)
            except ValidationError as e:
                raise ValueError(e)

            # Determine the extension (not bulletproof but good enough for now)
            url_path = urlparse(val).path
            path = Path(url_path)
            suffix = path.suffix
            if not suffix:
                raise ValueError('Unable to determine image extension.')

            # Download the image from the url
            try:
                response = requests.get(val, timeout=5)
                response.raise_for_status()
            except RequestException:
                raise ValueError('Unable to download image.')

            # Create a file obj with the downloaded image contents
            image = SimpleUploadedFile(
                name=f'{str(uuid.uuid4())}{suffix}',
                content=response.content,
                content_type=f'image/{suffix[1:]}'
            )

            # Validate the file is an image, convert to python and django under the hood will handle saving the image
            try:
                return forms.ImageField().clean(image)
            except ValidationError as e:
                raise ValueError(e)

        return val


class SeasonYearField(fields.Field):
    """
    This field handles importing/exporting using the season start year instead of the season id. BTSH seasons are
    within a single calendar year so this won't return multiple seasons for the same year.
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('column_name', 'season_year')
        kwargs.update({
            'widget': widgets.ForeignKeyWidget(Season, field='start__year'),
        })
        super().__init__(*args, **kwargs)


class TeamShortNameField(fields.Field):
    """
    This field handles importing/exporting using the team short name instead of the team id. Team short names are
    unique.
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('column_name', 'team_short_name')
        kwargs.update({
            'widget': widgets.ForeignKeyWidget(Team, field='short_name'),
        })
        super().__init__(*args, **kwargs)


class DivisionNameField(fields.Field):
    """
    This field handles importing/exporting using the division name instead of the division id. Division names are
    unique.
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('column_name', 'division_name')
        kwargs.update({
            'widget': widgets.ForeignKeyWidget(Division, field='name'),
        })
        super().__init__(*args, **kwargs)


class UserUsernameField(fields.Field):
    """
    This field handles importing/exporting using the user username instead of the user id. Usernames are unique and will
    generally be email addresses.
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('column_name', 'username')
        kwargs.update({
            'widget': widgets.ForeignKeyWidget(User, field='username'),
        })
        super().__init__(*args, **kwargs)


class GameDayDayField(fields.Field):
    """
    This field handles importing/exporting using the game day day instead of the game day id. Game day days are unique.
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('column_name', 'game_day')
        kwargs.update({
            'widget': widgets.ForeignKeyWidget(GameDay, field='day'),
        })
        super().__init__(*args, **kwargs)


class GamePlayerWidget(widgets.ForeignKeyWidget):
    def __init__(self, game_column_name, team_column_name, *args, **kwargs):
        self.game_column_name = game_column_name
        self.team_column_name = team_column_name
        super().__init__(GamePlayer, *args, **kwargs)

    def clean(self, value, row=None, **kwargs):
        if not value:
            return None

        game_id = row.get(self.game_column_name)
        team_short_name = row.get(self.team_column_name)
        try:
            return GamePlayer.objects.get(user__username=value, game_id=game_id, team__short_name=team_short_name)
        except GamePlayer.DoesNotExist:
            raise ValueError('Game player does not exist with this username.')


class GamePlayerField(fields.Field):
    """
    This field handles importing using a combination of username, game, team instead of the game player id. It's way
    easier for folks importing data to just provide the username instead of having to compute the game player id.
    """

    def __init__(self, game_column_name, team_column_name, *args, **kwargs):
        self.game_column_name = game_column_name
        self.team_column_name = team_column_name
        kwargs.update({
            'widget': GamePlayerWidget(game_column_name, team_column_name, field='id'),
        })
        super().__init__(*args, **kwargs)


class BaseModelResource(resources.ModelResource):
    @classmethod
    def widget_from_django_field(cls, f, default=widgets.Widget):
        widget = super().widget_from_django_field(f, default)
        if isinstance(f, models.ImageField):
            return ImageWidget
        return widget

    @classmethod
    def widget_kwargs_for_field(cls, field_name, django_field):
        kwargs = super().widget_kwargs_for_field(field_name, django_field)
        # Ensure booleans are handled as True/False instead of the 0/1 default
        if isinstance(django_field, models.BooleanField):
            kwargs.update({'coerce_to_string': False})
        return kwargs

    def __init__(self, user=None, **kwargs):
        # Exporting seems to init the resource class w/o passing the resource kwargs hence user needing to be none here
        self.user = user
        super().__init__(**kwargs)

    def save_instance(self, instance, is_create, row, **kwargs):
        # Other hooks either don't have is_create handy (before_save_instance) or don't run on bulk (do_instance_save)
        if is_create:
            instance.created_by = self.user
        else:
            instance.updated_by = self.user
        return super().save_instance(instance, is_create, row, **kwargs)

    class Meta:
        clean_model_instances = True
        model = None
        # Omitting BASE_MODEL_FIELDS for now since end users don't need to know about them
        fields = ('id',)
        skip_unchanged = True
