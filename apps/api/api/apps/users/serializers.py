from rest_framework import serializers

from common.serializers import BaseModelSerializer
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


class UserSeasonRegistrationReadOnlySerializer(BaseModelSerializer):
    user = UserReadOnlySerializer()
    season = SeasonReadOnlySerializer()
    team = TeamReadOnlySerializer(exclude=('seasons',))

    games_played = serializers.SerializerMethodField()
    goals = serializers.SerializerMethodField()
    primary_assists = serializers.SerializerMethodField()
    secondary_assists = serializers.SerializerMethodField()
    assists = serializers.SerializerMethodField()
    points = serializers.SerializerMethodField()
    place = serializers.SerializerMethodField()

    def get_games_played(self, obj):
        return getattr(obj, 'games_played', None)

    def get_goals(self, obj):
        return getattr(obj, 'goals', None)

    def get_primary_assists(self, obj):
        return getattr(obj, 'primary_assists', None)

    def get_secondary_assists(self, obj):
        return getattr(obj, 'secondary_assists', None)

    def get_assists(self, obj):
        return getattr(obj, 'assists', None)

    def get_points(self, obj):
        return getattr(obj, 'points', None)

    def get_place(self, obj):
        return getattr(obj, 'place', None)

    class Meta(BaseModelSerializer.Meta):
        model = UserSeasonRegistration
        fields = BaseModelSerializer.Meta.fields + (
            'user', 'season', 'team', 'is_captain', 'position', 'get_position_display', 'registered_at', 'location',
            'get_location_display', 'games_played', 'goals', 'primary_assists', 'secondary_assists', 'assists',
            'points', 'place',
        )
