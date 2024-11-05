from rest_framework import viewsets


class BaseModelReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    def get_queryset(self):
        return super().get_queryset().select_related('created_by', 'updated_by')
