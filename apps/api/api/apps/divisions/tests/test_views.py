from api.utils.testing import BaseTest


class TestDivisionViewSet(BaseTest):
    list_url = 'divisions:division-list'
    retrieve_url = 'divisions:division-detail'

    def test_list_permission(self, api_client, cmcdavid):
        # Anonymous
        assert api_client.get(self.reverse_api_url(url=self.list_url)).status_code == 200

        # Authenticated
        api_client.force_login(cmcdavid)
        assert api_client.get(self.reverse_api_url(url=self.list_url)).status_code == 200

    def test_list(self, api_client, settings, division1, division2, division3, placeholder_user):
        response = api_client.get(self.reverse_api_url(url=self.list_url))

        assert response.status_code == 200
        assert response.data == {
            'count': 3,
            'next': None,
            'previous': None,
            'results': [
                {
                    'created_by': self.format_created_by_updated_by(placeholder_user),
                    'updated_by': None,
                    'created_at': self.format_datetime(division1.created_at, tz=settings.DEFAULT_USER_TIME_ZONE),
                    'updated_at': self.format_datetime(division1.updated_at, tz=settings.DEFAULT_USER_TIME_ZONE),
                    'id': division1.id,
                    'name': 'Division 1',
                },
                {
                    'created_by': self.format_created_by_updated_by(placeholder_user),
                    'updated_by': None,
                    'created_at': self.format_datetime(division2.created_at, tz=settings.DEFAULT_USER_TIME_ZONE),
                    'updated_at': self.format_datetime(division2.updated_at, tz=settings.DEFAULT_USER_TIME_ZONE),
                    'id': division2.id,
                    'name': 'Division 2',
                },
                {
                    'created_by': self.format_created_by_updated_by(placeholder_user),
                    'updated_by': None,
                    'created_at': self.format_datetime(division3.created_at, tz=settings.DEFAULT_USER_TIME_ZONE),
                    'updated_at': self.format_datetime(division3.updated_at, tz=settings.DEFAULT_USER_TIME_ZONE),
                    'id': division3.id,
                    'name': 'Division 3',
                },
            ],
        }

    def test_retrieve_permission(self, api_client, cmcdavid, division1):
        url = self.reverse_api_url(url=self.retrieve_url, pk=division1.pk)

        # Anonymous
        assert api_client.get(url).status_code == 200

        # Authenticated
        api_client.force_login(cmcdavid)
        assert api_client.get(url).status_code == 200

    def test_retrieve(self, api_client, settings, division1, placeholder_user):
        response = api_client.get(self.reverse_api_url(url=self.retrieve_url, pk=division1.pk))

        assert response.status_code == 200
        assert response.data == {
            'created_by': self.format_created_by_updated_by(placeholder_user),
            'updated_by': None,
            'created_at': self.format_datetime(division1.created_at, tz=settings.DEFAULT_USER_TIME_ZONE),
            'updated_at': self.format_datetime(division1.updated_at, tz=settings.DEFAULT_USER_TIME_ZONE),
            'id': division1.id,
            'name': 'Division 1',
        }
