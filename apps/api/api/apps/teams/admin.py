from django.contrib import admin

from common.admin import BaseModelAdmin, BaseModelTabularInline
from .models import Team, TeamSeasonRegistration
from .resources import TeamResource, TeamSeasonRegistrationResource


class TeamSeasonRegistrationInline(BaseModelTabularInline):
    model = TeamSeasonRegistration
    fields = ('season', 'division',)
    autocomplete_fields = ('season', 'team', 'division',)
    ordering = ('-season__start', 'division', 'team',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('season', 'team', 'division')

@admin.register(Team)
class TeamAdmin(BaseModelAdmin):
    list_display = ('name', 'logo', 'jersey_colors', 'short_name')
    search_fields = ('name', 'short_name')
    ordering = ('name',)
    inlines = [TeamSeasonRegistrationInline]

    import_resource_classes = [TeamResource]
    export_resource_classes = [TeamResource]


@admin.register(TeamSeasonRegistration)
class TeamSeasonRegistration(BaseModelAdmin):
    # It doesn't make sense to include place here because the admin shows records across seasons, we could conditionally
    # include place when the user is filtering by season
    list_display = TeamSeasonRegistration.FIELDS
    list_filter = ('season', 'division', 'team',)
    search_fields = ('team__name',)
    ordering = ('-season__start', 'division', 'team',)
    autocomplete_fields = ('season', 'team', 'division',)
    readonly_fields = TeamSeasonRegistration.BASE_FIELDS

    import_resource_classes = [TeamSeasonRegistrationResource]
    export_resource_classes = [TeamSeasonRegistrationResource]
