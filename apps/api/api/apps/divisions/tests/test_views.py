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

    def test_list(self, api_client, division1, division2, division3, division1_expected_json, division2_expected_json,
                  division3_expected_json):
        response = api_client.get(self.reverse_api_url(url=self.list_url))

        assert response.status_code == 200
        self.assert_data(
            response.data,
            {
                'count': 3,
                'next': None,
                'previous': None,
                'results': [
                    division1_expected_json,
                    division2_expected_json,
                    division3_expected_json,
                ],
            })

    def test_retrieve_permission(self, api_client, cmcdavid, division1):
        url = self.reverse_api_url(url=self.retrieve_url, pk=division1.pk)

        # Anonymous
        assert api_client.get(url).status_code == 200

        # Authenticated
        api_client.force_login(cmcdavid)
        assert api_client.get(url).status_code == 200

    def test_retrieve(self, api_client, division1, division1_expected_json):
        response = api_client.get(self.reverse_api_url(url=self.retrieve_url, pk=division1.pk))

        assert response.status_code == 200
        self.assert_data(response.data, division1_expected_json)
