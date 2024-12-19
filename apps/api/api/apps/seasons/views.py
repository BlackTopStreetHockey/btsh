from common.views import BaseModelReadOnlyViewSet
from .filtersets import SeasonFilterSet
from .models import Season
from .serializers import SeasonReadOnlySerializer


class SeasonViewSet(BaseModelReadOnlyViewSet):
    queryset = Season.objects.all()
    serializer_class = SeasonReadOnlySerializer
    ordering = ('start',)
    ordering_fields = ('start', 'end',)
    filterset_class = SeasonFilterSet
