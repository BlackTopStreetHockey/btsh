from common.serializers import BaseModelSerializer
from .models import Season


class SeasonReadOnlySerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Season
        fields = BaseModelSerializer.Meta.fields + ('start', 'end', 'is_past', 'is_current', 'is_future', 'year')
