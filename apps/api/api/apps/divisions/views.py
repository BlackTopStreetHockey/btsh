from common.views import BaseModelReadOnlyViewSet
from .models import Division
from .serializers import DivisionReadOnlySerializer


class DivisionViewSet(BaseModelReadOnlyViewSet):
    queryset = Division.objects.all()
    serializer_class = DivisionReadOnlySerializer
    ordering = ('name',)
    ordering_fields = ('name',)
    search_fields = ('name',)
