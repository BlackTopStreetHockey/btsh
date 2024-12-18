from common.serializers import BaseReadOnlyModelSerializer
from .models import Season


class SeasonReadOnlySerializer(BaseReadOnlyModelSerializer):
    class Meta(BaseReadOnlyModelSerializer.Meta):
        model = Season
        fields = BaseReadOnlyModelSerializer.Meta.fields + ('start', 'end', 'is_past', 'is_current', 'is_future', 'year')
