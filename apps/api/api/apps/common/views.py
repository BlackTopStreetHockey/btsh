from rest_framework import viewsets

from .permissions import IsReadOnly


class BaseModelViewSet(viewsets.ModelViewSet):
    permission_classes = (IsReadOnly,)
    serializer_classes = {
        'create': None,
        'update': None,
        'partial_update': None,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action) or super().get_serializer_class()
