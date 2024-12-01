from common.views import BaseModelReadOnlyViewSet
from .filtersets import SeasonFilterSet, SeasonRegistrationFilterSet
from .models import Season, SeasonRegistration
from .serializers import SeasonReadOnlySerializer, SeasonRegistrationReadOnlySerializer


class SeasonViewSet(BaseModelReadOnlyViewSet):
    queryset = Season.objects.all()
    serializer_class = SeasonReadOnlySerializer
    ordering = ('start',)
    ordering_fields = ('start', 'end',)
    filterset_class = SeasonFilterSet


class SeasonRegistrationViewSet(BaseModelReadOnlyViewSet):
    queryset = SeasonRegistration.objects.all().select_related('user', 'season', 'team')
    serializer_class = SeasonRegistrationReadOnlySerializer
    ordering = ('season', 'team', 'user')
    ordering_fields = ('season', 'team',)
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'team__name',)
    filterset_class = SeasonRegistrationFilterSet
