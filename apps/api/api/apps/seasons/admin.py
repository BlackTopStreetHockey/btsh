from django.contrib import admin, messages

from common.admin import BaseModelAdmin
from games.models import Game
from teams.admin import TeamSeasonRegistrationInline
from teams.utils import calculate_team_season_registration_stats
from .models import Season


@admin.register(Season)
class SeasonAdmin(BaseModelAdmin):
    list_display = ('start', 'end', 'is_past', 'is_current', 'is_future',)
    list_filter = ('start', 'end',)
    search_fields = ('start', 'end')
    ordering = ('start', 'end')
    inlines = [TeamSeasonRegistrationInline]
    actions = ['calculate_team_season_registration_stats']

    @admin.display(boolean=True)
    def is_past(self, obj):
        return obj.is_past

    @admin.display(boolean=True)
    def is_current(self, obj):
        return obj.is_current

    @admin.display(boolean=True)
    def is_future(self, obj):
        return obj.is_future

    @admin.action(description='Recalculate season stats')
    def calculate_team_season_registration_stats(self, request, queryset):
        for season in queryset:
            calculate_team_season_registration_stats(game_type=Game.REGULAR, limit_to_season=season, debug=True)
        self.message_user(request, f'Successfully recalculated stats for {queryset.count()} seasons.', messages.SUCCESS)
