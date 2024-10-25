from django.contrib import admin

from common.admin import BaseModelAdmin
from .models import Game, GameDay


@admin.register(GameDay)
class GameDayAdmin(BaseModelAdmin):
    list_display = ('day', 'season', 'opening_team', 'closing_team')
    list_filter = ('day', 'season', 'opening_team', 'closing_team')
    search_fields = ('opening_team__name', 'closing_team__name')
    ordering = ('-season__start', 'day',)
    autocomplete_fields = ('season', 'opening_team', 'closing_team')


@admin.register(Game)
class GameAdmin(BaseModelAdmin):
    list_display = ('game_day', 'start', 'end', 'duration', 'home_team', 'away_team', 'location', 'court')
    list_filter = ('court', 'home_team', 'away_team', 'location')
    search_fields = ('home_team__name', 'away_team__name', 'court')
    ordering = ('-game_day__day', 'start')
    autocomplete_fields = ('game_day', 'home_team', 'away_team')
    readonly_fields = ('end',)
