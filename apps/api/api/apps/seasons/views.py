from common.views import BaseModelViewSet
from .filtersets import SeasonFilterSet
from .models import Season
from .serializers import SeasonReadOnlySerializer


class SeasonViewSet(BaseModelViewSet):
    queryset = Season.objects.all()
    serializer_class = SeasonReadOnlySerializer
    ordering = ('start',)
    ordering_fields = ('start', 'end',)
    filterset_class = SeasonFilterSet
