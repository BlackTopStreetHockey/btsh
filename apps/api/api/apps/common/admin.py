from django.contrib import admin
from import_export.admin import ExportActionMixin, ImportExportModelAdmin


class BaseModelAdmin(ImportExportModelAdmin, ExportActionMixin):
    date_hierarchy = 'created_at'
    list_display_links = ('id',)
    list_select_related = True

    import_resource_classes = None
    export_resource_classes = None

    def get_list_display(self, request):
        list_display = super().get_list_display(request)
        # TODO including created_by and updated_by here results in N+1 sql queries, select related isn't working and
        # i'm not sure why
        return ['id', *list_display, 'created_at', 'updated_at']

    def get_list_filter(self, request):
        list_filter = super().get_list_filter(request)
        return [*list_filter, 'created_at']

    def get_search_fields(self, request):
        search_fields = super().get_search_fields(request)
        return ['id', *search_fields]

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(obj)
        return [*readonly_fields, 'created_by', 'updated_by', 'created_at', 'updated_at']

    def save_model(self, request, obj, form, change):
        user = request.user

        if change:
            obj.updated_by = user
        else:
            obj.created_by = user

        super().save_model(request, obj, form, change)

    # Django import export overrides
    def get_import_resource_kwargs(self, request, **kwargs):
        import_resource_kwargs = super().get_import_resource_kwargs(request, **kwargs)
        import_resource_kwargs.update({'user': request.user})
        return import_resource_kwargs

    def get_import_resource_classes(self, request):
        import_resource_classes = getattr(self, 'import_resource_classes', None)
        return import_resource_classes or super().get_import_resource_classes(request)

    def get_export_resource_kwargs(self, request, **kwargs):
        export_resource_kwargs = super().get_export_resource_kwargs(request, **kwargs)
        export_resource_kwargs.update({'user': request.user})
        return export_resource_kwargs

    def get_export_resource_classes(self, request):
        export_resource_classes = getattr(self, 'export_resource_classes', None)
        return export_resource_classes or super().get_export_resource_classes(request)


class BaseModelTabularInline(admin.TabularInline):
    extra = 0
    exclude = ('created_by', 'updated_by')
