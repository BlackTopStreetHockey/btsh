from django.contrib import admin


class BaseModelAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display_links = ('id',)
    readonly_fields = ('created_at', 'updated_at')

    def get_list_display(self, request):
        list_display = super().get_list_display(request)
        return ['id', *list_display, 'created_at', 'updated_at']

    def get_list_filter(self, request):
        list_filter = super().get_list_filter(request)
        return [*list_filter, 'created_at']

    def get_search_fields(self, request):
        search_fields = super().get_search_fields(request)
        return ['id', *search_fields]
