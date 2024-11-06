from api.utils.testing import BaseTest


class TestTeamViewSet(BaseTest):
    list_url = 'teams:team-list'
    retrieve_url = 'teams:team-detail'

    def test_list(self, api_client, settings, corlears_hookers, lbs, placeholder_user_expected_json):
        response = api_client.get(self.reverse_api_url(url=self.list_url))

        assert response.status_code == 200
        assert response.data == {
            'count': 2,
            'next': None,
            'previous': None,
            'results': [
                {
                    'created_by': placeholder_user_expected_json(settings.DEFAULT_USER_TIME_ZONE),
                    'updated_by': None,
                    'created_at': self.format_datetime(corlears_hookers.created_at, tz=settings.DEFAULT_USER_TIME_ZONE),
                    'updated_at': self.format_datetime(corlears_hookers.updated_at, tz=settings.DEFAULT_USER_TIME_ZONE),
                    'id': corlears_hookers.id,
                    'name': 'Corlears Hookers',
                    'logo': f'http://testserver/media/{corlears_hookers.logo.name}',
                    'jersey_colors': ['white', 'purple'],
                },
                {
                    'created_by': placeholder_user_expected_json(settings.DEFAULT_USER_TIME_ZONE),
                    'updated_by': None,
                    'created_at': self.format_datetime(lbs.created_at, tz=settings.DEFAULT_USER_TIME_ZONE),
                    'updated_at': self.format_datetime(lbs.updated_at, tz=settings.DEFAULT_USER_TIME_ZONE),
                    'id': lbs.id,
                    'name': 'Lbs',
                    'logo': f'http://testserver/media/{lbs.logo.name}',
                    'jersey_colors': None,
                },
            ],
        }

    def test_retrieve(self, api_client, settings, corlears_hookers, placeholder_user_expected_json):
        response = api_client.get(self.reverse_api_url(url=self.retrieve_url, pk=corlears_hookers.pk))

        assert response.status_code == 200
        assert response.data == {
            'created_by': placeholder_user_expected_json(settings.DEFAULT_USER_TIME_ZONE),
            'updated_by': None,
            'created_at': self.format_datetime(corlears_hookers.created_at, tz=settings.DEFAULT_USER_TIME_ZONE),
            'updated_at': self.format_datetime(corlears_hookers.updated_at, tz=settings.DEFAULT_USER_TIME_ZONE),
            'id': corlears_hookers.id,
            'name': 'Corlears Hookers',
            'logo': f'http://testserver/media/{corlears_hookers.logo.name}',
            'jersey_colors': ['white', 'purple'],
        }
