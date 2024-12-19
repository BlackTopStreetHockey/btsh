from common.views import BaseModelReadOnlyViewSet
from .filtersets import UserSeasonRegistrationFilterSet
from .models import UserSeasonRegistration
from .serializers import UserSeasonRegistrationReadOnlySerializer


class UserSeasonRegistrationViewSet(BaseModelReadOnlyViewSet):
    queryset = UserSeasonRegistration.objects.all().select_related('user', 'season', 'team')
    serializer_class = UserSeasonRegistrationReadOnlySerializer
    ordering = ('season', 'team', 'user')
    ordering_fields = ('season', 'team',)
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'team__name',)
    filterset_class = UserSeasonRegistrationFilterSet
