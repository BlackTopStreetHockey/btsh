from datetime import datetime, timezone

from api.utils.testing import BaseTest


class TestSeasonViewSet(BaseTest):
    list_url = 'seasons:season-list'
    retrieve_url = 'seasons:season-detail'

    def test_list_permission(self, api_client, cmcdavid):
        # Anonymous
        assert api_client.get(self.reverse_api_url(url=self.list_url)).status_code == 200

        # Authenticated
        api_client.force_login(cmcdavid)
        assert api_client.get(self.reverse_api_url(url=self.list_url)).status_code == 200

    def test_list(self, api_client, mocker, season_2024, season_2022_expected_json, season_2023_expected_json,
                  season_2024_expected_json):
        mocker.patch('django.utils.timezone.now', return_value=datetime(
            year=season_2024.start.year,
            month=5,
            day=20,
            hour=12,
            minute=3,
            second=9,
            tzinfo=timezone.utc,
        ))

        response = api_client.get(self.reverse_api_url(url=self.list_url))

        assert response.status_code == 200
        self.assert_data(
            response.data,
            {
                'count': 3,
                'next': None,
                'previous': None,
                'results': [
                    self.clean_data(season_2022_expected_json(is_past=True, is_current=False, is_future=False)),
                    self.clean_data(season_2023_expected_json(is_past=True, is_current=False, is_future=False)),
                    self.clean_data(season_2024_expected_json(is_past=False, is_current=True, is_future=False)),
                ],
            }
        )

    def test_retrieve_permission(self, api_client, cmcdavid, season_2024):
        url = self.reverse_api_url(url=self.retrieve_url, pk=season_2024.pk)

        # Anonymous
        assert api_client.get(url).status_code == 200

        # Authenticated
        api_client.force_login(cmcdavid)
        assert api_client.get(url).status_code == 200

    def test_retrieve(self, api_client, season_2024, season_2024_expected_json):
        response = api_client.get(self.reverse_api_url(url=self.retrieve_url, pk=season_2024.pk))

        assert response.status_code == 200
        self.assert_data(response.data, season_2024_expected_json(is_past=True, is_current=False, is_future=False))
