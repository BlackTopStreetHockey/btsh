from django.contrib import admin

from common.admin import BaseModelAdmin
from common.resources import BaseModelResource
from .models import Division


class DivisionResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        model = Division
        fields = BaseModelResource.Meta.fields + ('name',)


@admin.register(Division)
class DivisionAdmin(BaseModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)
    import_resource_classes = [DivisionResource]
    export_resource_classes = [DivisionResource]
