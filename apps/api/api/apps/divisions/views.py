from common.views import BaseModelViewSet
from .models import Division
from .serializers import DivisionReadOnlySerializer


class DivisionViewSet(BaseModelViewSet):
    queryset = Division.objects.all()
    serializer_class = DivisionReadOnlySerializer
    ordering = ('name',)
    ordering_fields = ('name',)
    search_fields = ('name',)
