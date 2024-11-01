from api.utils.testing import BaseTest


class TestDivisionViewSet(BaseTest):
    list_url = 'divisions:division-list'
    retrieve_url = 'divisions:division-detail'

    def test_list(self, api_client, settings, division1, division2, division3, placeholder_user_expected_json):
        response = api_client.get(self.reverse_api_url(url=self.list_url))

        assert response.status_code == 200
        assert response.data == {
            'count': 3,
            'next': None,
            'previous': None,
            'results': [
                {
                    'created_by': placeholder_user_expected_json(settings.DEFAULT_USER_TIME_ZONE),
                    'updated_by': None,
                    'created_at': self.format_datetime(division1.created_at, tz=settings.DEFAULT_USER_TIME_ZONE),
                    'updated_at': self.format_datetime(division1.updated_at, tz=settings.DEFAULT_USER_TIME_ZONE),
                    'id': division1.id,
                    'name': 'Division 1',
                },
                {
                    'created_by': placeholder_user_expected_json(settings.DEFAULT_USER_TIME_ZONE),
                    'updated_by': None,
                    'created_at': self.format_datetime(division2.created_at, tz=settings.DEFAULT_USER_TIME_ZONE),
                    'updated_at': self.format_datetime(division2.updated_at, tz=settings.DEFAULT_USER_TIME_ZONE),
                    'id': division2.id,
                    'name': 'Division 2',
                },
                {
                    'created_by': placeholder_user_expected_json(settings.DEFAULT_USER_TIME_ZONE),
                    'updated_by': None,
                    'created_at': self.format_datetime(division3.created_at, tz=settings.DEFAULT_USER_TIME_ZONE),
                    'updated_at': self.format_datetime(division3.updated_at, tz=settings.DEFAULT_USER_TIME_ZONE),
                    'id': division3.id,
                    'name': 'Division 3',
                },
            ],
        }

    def test_retrieve(self, api_client, settings, division1, placeholder_user_expected_json):
        response = api_client.get(self.reverse_api_url(url=self.retrieve_url, pk=division1.pk))

        assert response.status_code == 200
        assert response.data == {
            'created_by': placeholder_user_expected_json(settings.DEFAULT_USER_TIME_ZONE),
            'updated_by': None,
            'created_at': self.format_datetime(division1.created_at, tz=settings.DEFAULT_USER_TIME_ZONE),
            'updated_at': self.format_datetime(division1.updated_at, tz=settings.DEFAULT_USER_TIME_ZONE),
            'id': division1.id,
            'name': 'Division 1',
        }
