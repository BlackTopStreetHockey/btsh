from common.serializers import BaseModelSerializer
from .models import Division


class DivisionReadOnlySerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Division
        fields = BaseModelSerializer.Meta.fields + ('name',)
