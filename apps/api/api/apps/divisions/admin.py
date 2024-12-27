from django.contrib import admin

from common.admin import BaseModelAdmin
from .models import Division
from .resources import DivisionResource


@admin.register(Division)
class DivisionAdmin(BaseModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)
    import_resource_classes = [DivisionResource]
    export_resource_classes = [DivisionResource]
