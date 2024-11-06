from api.utils.testing import BaseTest
from teams.serializers import TeamReadOnlySerializer


class TestTeamReadOnlySerializer(BaseTest):
    def test_serialize(self, settings, corlears_hookers, placeholder_user_expected_json):
        s = TeamReadOnlySerializer(corlears_hookers)

        assert s.data == {
            'created_by': placeholder_user_expected_json(settings.DEFAULT_USER_TIME_ZONE),
            'updated_by': None,
            'created_at': self.format_datetime(corlears_hookers.created_at, tz=settings.DEFAULT_USER_TIME_ZONE),
            'updated_at': self.format_datetime(corlears_hookers.updated_at, tz=settings.DEFAULT_USER_TIME_ZONE),
            'id': corlears_hookers.id,
            'name': 'Corlears Hookers',
            # logo has a randomly generated filename, an explicit check for the path would be hard and mocking doesn't
            # seem worth it
            'logo': f'/media/{corlears_hookers.logo.name}',
            'jersey_colors': ['white', 'purple'],
        }
