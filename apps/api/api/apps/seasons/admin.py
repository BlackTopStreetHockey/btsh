from django.contrib import admin

from common.admin import BaseModelAdmin
from teams.admin import TeamSeasonRegistrationInline
from .models import Season


@admin.register(Season)
class SeasonAdmin(BaseModelAdmin):
    list_display = ('start', 'end', 'is_past', 'is_current', 'is_future',)
    list_filter = ('start', 'end',)
    search_fields = ('start', 'end')
    ordering = ('start', 'end')
    inlines = [TeamSeasonRegistrationInline]

    @admin.display(boolean=True)
    def is_past(self, obj):
        return obj.is_past

    @admin.display(boolean=True)
    def is_current(self, obj):
        return obj.is_current

    @admin.display(boolean=True)
    def is_future(self, obj):
        return obj.is_future
