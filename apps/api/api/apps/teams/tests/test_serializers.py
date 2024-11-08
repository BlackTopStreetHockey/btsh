from api.utils.testing import BaseTest
from teams.serializers import TeamReadOnlySerializer


class TestTeamReadOnlySerializer(BaseTest):
    def test_serialize(self, settings, corlears_hookers, corlears_hookers_expected_json):
        s = TeamReadOnlySerializer(corlears_hookers)

        assert s.data == corlears_hookers_expected_json(tz=settings.DEFAULT_USER_TIME_ZONE)
