from common.views import BaseModelReadOnlyViewSet
from .models import Team
from .serializers import TeamReadOnlySerializer
from rest_framework import viewsets, generics, mixins
from rest_framework.exceptions import NotFound
from django.db.models import Q
from games.serializers import GameReadOnlySerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet


class TeamViewSet(BaseModelReadOnlyViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamReadOnlySerializer
    ordering = ('name',)
    ordering_fields = ('name', 'short_name')
    search_fields = ('name', 'short_name')


class TeamDetailByShortNameView(mixins.RetrieveModelMixin, GenericViewSet):
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

    @action(detail=True, methods=['get'])
    def schedule(self, request, short_name=None):
        team = self.get_object()
        games = (team.games_home.all() | team.games_away.all())\
            .select_related('home_team', 'away_team')\
            .order_by('-start')
        serializer = GameReadOnlySerializer(games, many=True)
        return Response(serializer.data)
