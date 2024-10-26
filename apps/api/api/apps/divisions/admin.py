from django.contrib import admin

from common.admin import BaseModelAdmin
from .models import Division


@admin.register(Division)
class DivisionAdmin(BaseModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)
