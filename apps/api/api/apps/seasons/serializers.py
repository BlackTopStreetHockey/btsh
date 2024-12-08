from common.serializers import BaseReadOnlyModelSerializer
from teams.serializers import TeamReadOnlySerializer
from users.serializers import UserReadOnlySerializer
from .models import Season, SeasonRegistration


class SeasonReadOnlySerializer(BaseReadOnlyModelSerializer):
    class Meta(BaseReadOnlyModelSerializer.Meta):
        model = Season
        fields = BaseReadOnlyModelSerializer.Meta.fields + ('start', 'end', 'is_past', 'is_current', 'is_future', 'year')


class SeasonRegistrationReadOnlySerializer(BaseReadOnlyModelSerializer):
    user = UserReadOnlySerializer()
    season = SeasonReadOnlySerializer()
    team = TeamReadOnlySerializer()

    class Meta(BaseReadOnlyModelSerializer.Meta):
        model = SeasonRegistration
        fields = BaseReadOnlyModelSerializer.Meta.fields + (
            'user', 'season', 'team', 'is_captain', 'position', 'get_position_display', 'registered_at', 'location',
            'get_location_display',
        )
