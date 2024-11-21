from common.views import BaseModelReadOnlyViewSet
from .models import Team
from .serializers import TeamReadOnlySerializer


class TeamViewSet(BaseModelReadOnlyViewSet):
    queryset = Team.objects.all()
    lookup_field = 'short_name'
    serializer_class = TeamReadOnlySerializer
    ordering = ('name',)
    ordering_fields = ('name', 'short_name')
    search_fields = ('name', 'short_name')
