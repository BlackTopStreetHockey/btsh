from common.serializers import BaseReadOnlyModelSerializer
from .models import Division


class DivisionReadOnlySerializer(BaseReadOnlyModelSerializer):
    class Meta(BaseReadOnlyModelSerializer.Meta):
        model = Division
        fields = BaseReadOnlyModelSerializer.Meta.fields + ('name', 'short_name')
