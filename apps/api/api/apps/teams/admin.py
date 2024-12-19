from django.contrib import admin

from common.admin import BaseModelAdmin, BaseModelTabularInline
from .models import Team, TeamSeasonRegistration


class TeamSeasonRegistrationInline(BaseModelTabularInline):
    model = TeamSeasonRegistration
    autocomplete_fields = ('season', 'team', 'division',)
    ordering = ('-season__start', 'division', 'team',)


@admin.register(Team)
class TeamAdmin(BaseModelAdmin):
    list_display = ('name', 'logo', 'jersey_colors', 'short_name')
    search_fields = ('name', 'short_name')
    ordering = ('name',)
    inlines = [TeamSeasonRegistrationInline]


@admin.register(TeamSeasonRegistration)
class TeamSeasonRegistration(BaseModelAdmin):
    list_display = ('season', 'team', 'division', 'home_games_played', 'away_games_played', 'games_played')
    list_filter = ('season', 'division', 'team',)
    search_fields = ('team__name',)
    ordering = ('-season__start', 'division', 'team',)
    autocomplete_fields = ('season', 'team', 'division',)
