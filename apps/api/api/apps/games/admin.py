from django.contrib import admin

from common.admin import BaseModelAdmin, BaseModelTabularInline
from .models import Game, GameDay, GameGoal, GamePlayer, GameReferee, GameResultsEnum
from .resources import (
    GameDayResource,
    GameGoalImportResource,
    GameGoalExportResource,
    GamePlayerResource,
    GameRefereeResource,
    GameResource
)


class GameInline(BaseModelTabularInline):
    model = Game
    autocomplete_fields = ('home_team', 'away_team',)
    readonly_fields = ('end',)
    ordering = ('start', '-type', 'status',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related()


class GameRefereeInline(BaseModelTabularInline):
    model = GameReferee
    autocomplete_fields = ('user',)
    ordering = ('type', 'user__email',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related()


class GamePlayerInline(BaseModelTabularInline):
    model = GamePlayer
    autocomplete_fields = ('user', 'team',)
    ordering = ('team__name', 'user__email')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related()


class GameGoalInline(BaseModelTabularInline):
    model = GameGoal
    autocomplete_fields = ('team', 'scored_by', 'assisted_by1', 'assisted_by2',)
    ordering = ('period', 'team__name')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related()


@admin.register(GameDay)
class GameDayAdmin(BaseModelAdmin):
    list_display = ('day', 'season', 'opening_team', 'closing_team')
    list_filter = ('day', 'season', 'opening_team', 'closing_team')
    search_fields = ('opening_team__name', 'closing_team__name', 'season__start__year', 'season__end__year')
    ordering = ('-season__start', 'day',)
    autocomplete_fields = ('season', 'opening_team', 'closing_team')
    inlines = [GameInline]

    import_resource_classes = [GameDayResource]
    export_resource_classes = [GameDayResource]


class GameResultListFilter(admin.SimpleListFilter):
    title = 'Result'
    parameter_name = 'result'

    def lookups(self, request, model_admin):
        return [
            (GameResultsEnum.FINAL.value, GameResultsEnum.FINAL.label),
            (GameResultsEnum.FINAL_OT.value, GameResultsEnum.FINAL_OT.label),
            (GameResultsEnum.FINAL_SO.value, GameResultsEnum.FINAL_SO.label),
        ]

    def queryset(self, request, queryset):
        return queryset.filter(result=self.value()) if self.value() else queryset


@admin.register(Game)
class GameAdmin(BaseModelAdmin):
    list_display = (
        'game_day', 'start', 'status', 'type', 'home_team_display', 'away_team_display', 'get_result_display', 'court',
        'location', 'end', 'duration',
    )
    list_filter = (
        'game_day__day', 'game_day__season', 'status', GameResultListFilter, 'court', 'type', 'home_team', 'away_team',
        'location'
    )
    search_fields = ('game_day__day', 'start', 'home_team__name', 'away_team__name', 'court')
    ordering = ('-game_day__day', 'start')
    autocomplete_fields = ('game_day', 'home_team', 'away_team')
    readonly_fields = ('end', 'home_team_display', 'away_team_display', 'get_result_display')
    inlines = [GameGoalInline, GameRefereeInline, GamePlayerInline]

    import_resource_classes = [GameResource]
    export_resource_classes = [GameResource]

    @admin.display(description='Home Team')
    def home_team_display(self, obj):
        return obj.home_team_display

    @admin.display(description='Away Team')
    def away_team_display(self, obj):
        return obj.away_team_display

    @admin.display(description='Result')
    def get_result_display(self, obj):
        return obj.get_result_display

    def get_queryset(self, request):
        return super().get_queryset(request).with_scores()


@admin.register(GameReferee)
class GameRefereeAdmin(BaseModelAdmin):
    list_display = ('game', 'user', 'type')
    list_filter = ('game__game_day__season', 'game__status', 'game__type', 'type',)
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'game__id',)
    ordering = ('-game__game_day__day', 'game__start',)
    autocomplete_fields = ('game', 'user',)

    import_resource_classes = [GameRefereeResource]
    export_resource_classes = [GameRefereeResource]


@admin.register(GamePlayer)
class GamePlayerAdmin(BaseModelAdmin):
    list_display = ('game', 'user', 'team', 'is_substitute', 'is_goalie')
    list_filter = ('game__game_day__season', 'game__status', 'game__type', 'is_substitute', 'is_goalie', 'team')
    search_fields = (
        'user__username', 'user__email', 'user__first_name', 'user__last_name', 'team__name', 'game__game_day__day',
        'game__id',
    )
    ordering = ('-game__game_day__day', 'game__start',)
    autocomplete_fields = ('game', 'user', 'team')

    import_resource_classes = [GamePlayerResource]
    export_resource_classes = [GamePlayerResource]


@admin.register(GameGoal)
class GameGoalAdmin(BaseModelAdmin):
    list_display = (
        'game', 'team', 'team_against', 'period', 'scored_by_name', 'assisted_by1_name', 'assisted_by2_name',
    )
    list_filter = ('game__game_day__season', 'game__status', 'game__type', 'period', 'team', 'team_against')
    search_fields = (
        'scored_by__user__username',
        'scored_by__user__email',
        'scored_by__user__first_name',
        'scored_by__user__last_name',
        'assisted_by1__user__username',
        'assisted_by1__user__email',
        'assisted_by1__user__first_name',
        'assisted_by1__user__last_name',
        'assisted_by2__user__username',
        'assisted_by2__user__email',
        'assisted_by2__user__first_name',
        'assisted_by2__user__last_name',
        'team__name',
        'game__id',
    )
    ordering = ('-game__game_day__day', 'game__start', 'team', 'period')
    autocomplete_fields = ('game', 'team', 'team_against', 'scored_by', 'assisted_by1', 'assisted_by2')

    import_resource_classes = [GameGoalImportResource]
    export_resource_classes = [GameGoalExportResource]

    @admin.display(description='Scored By')
    def scored_by_name(self, obj):
        return obj.scored_by.user.get_full_name()

    @admin.display(description='Assisted By1')
    def assisted_by1_name(self, obj):
        return obj.assisted_by1.user.get_full_name() if obj.assisted_by1 else None

    @admin.display(description='Assisted By2')
    def assisted_by2_name(self, obj):
        return obj.assisted_by2.user.get_full_name() if obj.assisted_by2 else None

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'game__game_day', 'game__home_team', 'game__away_team', 'team', 'team_against', 'scored_by__user',
            'assisted_by1__user', 'assisted_by2__user',
        )
