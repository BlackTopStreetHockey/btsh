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
    list_display = TeamSeasonRegistration.FIELDS
    list_filter = ('season', 'division', 'team',)
    search_fields = ('team__name',)
    ordering = ('-season__start', 'division', 'team',)
    autocomplete_fields = ('season', 'team', 'division',)
    readonly_fields = (
        # Games played
        'home_games_played', 'away_games_played',
        # Home wins, losses, ties
        'home_regulation_wins', 'home_regulation_losses',
        'home_overtime_wins', 'home_overtime_losses',
        'home_shootout_wins', 'home_shootout_losses',
        'home_ties',
        # Away wins, losses, ties
        'away_regulation_wins', 'away_regulation_losses',
        'away_overtime_wins', 'away_overtime_losses',
        'away_shootout_wins', 'away_shootout_losses',
        'away_ties',
        # Totals
        'games_played',
        'home_wins', 'home_losses',
        'away_wins', 'away_losses',
        'regulation_wins', 'regulation_losses',
        'overtime_wins', 'overtime_losses',
        'shootout_wins', 'shootout_losses',
        'wins', 'losses', 'ties',
    )
