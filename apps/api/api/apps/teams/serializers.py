from common.serializers import BaseReadOnlyModelSerializer
from .models import Team


class TeamReadOnlySerializer(BaseReadOnlyModelSerializer):
    class Meta(BaseReadOnlyModelSerializer.Meta):
        model = Team
        fields = BaseReadOnlyModelSerializer.Meta.fields + ('name', 'logo', 'jersey_colors')
