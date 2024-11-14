from common.views import BaseModelReadOnlyViewSet
from .models import Team
from .serializers import TeamReadOnlySerializer
from rest_framework import viewsets, generics
from rest_framework.exceptions import NotFound


class TeamViewSet(BaseModelReadOnlyViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamReadOnlySerializer
    ordering = ('name',)
    ordering_fields = ('name', 'short_name')
    search_fields = ('name', 'short_name')


class TeamDetailByShortNameView(generics.RetrieveAPIView):
    serializer_class = TeamReadOnlySerializer
    lookup_field = 'short_name'
    lookup_url_kwarg = 'short_name'
    queryset = Team.objects.all()

    def get_object(self):
        short_name = self.kwargs.get('short_name')
        try:
            return Team.objects.get(short_name=short_name)
        except Team.DoesNotExist:
            raise NotFound(f"No team found with short name: {short_name}")
