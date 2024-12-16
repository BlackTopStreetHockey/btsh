from rest_framework import serializers

from common.serializers import BaseReadOnlyModelSerializer
from seasons.serializers import SeasonReadOnlySerializer
from teams.serializers import TeamReadOnlySerializer
from .models import User, UserSeasonRegistration


class UserReadOnlySerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return obj.get_full_name()

    class Meta:
        model = User
        # Intentionally omit username/email so we don't include more PII than we need to
        fields = ('id', 'first_name', 'last_name', 'full_name', 'date_joined', 'gender', 'get_gender_display')


class UserSeasonRegistrationReadOnlySerializer(BaseReadOnlyModelSerializer):
    user = UserReadOnlySerializer()
    season = SeasonReadOnlySerializer()
    team = TeamReadOnlySerializer()

    class Meta(BaseReadOnlyModelSerializer.Meta):
        model = UserSeasonRegistration
        fields = BaseReadOnlyModelSerializer.Meta.fields + (
            'user', 'season', 'team', 'is_captain', 'position', 'get_position_display', 'registered_at', 'location',
            'get_location_display',
        )
