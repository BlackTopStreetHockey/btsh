from django.contrib import admin

from common.admin import BaseModelAdmin, BaseModelTabularInline
from .models import Game, GameDay


class GameInline(BaseModelTabularInline):
    model = Game
    autocomplete_fields = ('home_team', 'away_team',)
    readonly_fields = ('end',)
    ordering = ('start',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related()


@admin.register(GameDay)
class GameDayAdmin(BaseModelAdmin):
    list_display = ('day', 'season', 'opening_team', 'closing_team')
    list_filter = ('day', 'season', 'opening_team', 'closing_team')
    search_fields = ('opening_team__name', 'closing_team__name')
    ordering = ('-season__start', 'day',)
    autocomplete_fields = ('season', 'opening_team', 'closing_team')
    inlines = [GameInline]


@admin.register(Game)
class GameAdmin(BaseModelAdmin):
    list_display = ('game_day', 'start', 'end', 'duration', 'home_team', 'away_team', 'location', 'court')
    list_filter = ('game_day__day', 'game_day__season', 'court', 'home_team', 'away_team', 'location')
    search_fields = ('home_team__name', 'away_team__name', 'court')
    ordering = ('-game_day__day', 'start')
    autocomplete_fields = ('game_day', 'home_team', 'away_team')
    readonly_fields = ('end',)
