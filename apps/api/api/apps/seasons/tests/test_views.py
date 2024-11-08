from datetime import datetime, timezone

from api.utils.testing import BaseTest


class TestSeasonViewSet(BaseTest):
    list_url = 'seasons:season-list'
    retrieve_url = 'seasons:season-detail'

    def test_list(self, api_client, settings, mocker, season_2024, season_2022_expected_json, season_2023_expected_json,
                  season_2024_expected_json, placeholder_user_expected_json):
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
        assert response.data == {
            'count': 3,
            'next': None,
            'previous': None,
            'results': [
                season_2022_expected_json(
                    is_past=True, is_current=False, is_future=False, tz=settings.DEFAULT_USER_TIME_ZONE
                ),
                season_2023_expected_json(
                    is_past=True, is_current=False, is_future=False, tz=settings.DEFAULT_USER_TIME_ZONE
                ),
                season_2024_expected_json(
                    is_past=False, is_current=True, is_future=False, tz=settings.DEFAULT_USER_TIME_ZONE
                )
            ],
        }

    def test_retrieve(self, api_client, settings, season_2024, season_2024_expected_json):
        response = api_client.get(self.reverse_api_url(url=self.retrieve_url, pk=season_2024.pk))

        assert response.status_code == 200
        assert response.data == season_2024_expected_json(
            is_past=True, is_current=False, is_future=False, tz=settings.DEFAULT_USER_TIME_ZONE
        )
