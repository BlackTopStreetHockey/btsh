from django.contrib import admin

from common.admin import BaseModelAdmin
from .models import Team


@admin.register(Team)
class TeamAdmin(BaseModelAdmin):
    list_display = ('name', 'logo', 'jersey_colors', 'short_name')
    search_fields = ('name', 'short_name')
    ordering = ('name',)
