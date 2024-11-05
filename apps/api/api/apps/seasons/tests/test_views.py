from datetime import datetime, timezone

from api.utils.testing import BaseTest


class TestSeasonViewSet(BaseTest):
    list_url = 'seasons:season-list'
    retrieve_url = 'seasons:season-detail'

    def test_list(self, api_client, settings, mocker, season_2022, season_2023, season_2024,
                  placeholder_user_expected_json):
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
                {
                    'created_by': placeholder_user_expected_json(settings.DEFAULT_USER_TIME_ZONE),
                    'updated_by': None,
                    'created_at': self.format_datetime(season_2022.created_at, tz=settings.DEFAULT_USER_TIME_ZONE),
                    'updated_at': self.format_datetime(season_2022.updated_at, tz=settings.DEFAULT_USER_TIME_ZONE),
                    'id': season_2022.id,
                    'start': '2022-03-31',
                    'end': '2022-10-31',
                    'is_past': True,
                    'is_current': False,
                    'is_future': False,
                },
                {
                    'created_by': placeholder_user_expected_json(settings.DEFAULT_USER_TIME_ZONE),
                    'updated_by': None,
                    'created_at': self.format_datetime(season_2023.created_at, tz=settings.DEFAULT_USER_TIME_ZONE),
                    'updated_at': self.format_datetime(season_2023.updated_at, tz=settings.DEFAULT_USER_TIME_ZONE),
                    'id': season_2023.id,
                    'start': '2023-03-31',
                    'end': '2023-10-31',
                    'is_past': True,
                    'is_current': False,
                    'is_future': False,
                },
                {
                    'created_by': placeholder_user_expected_json(settings.DEFAULT_USER_TIME_ZONE),
                    'updated_by': None,
                    'created_at': self.format_datetime(season_2024.created_at, tz=settings.DEFAULT_USER_TIME_ZONE),
                    'updated_at': self.format_datetime(season_2024.updated_at, tz=settings.DEFAULT_USER_TIME_ZONE),
                    'id': season_2024.id,
                    'start': '2024-03-31',
                    'end': '2024-10-31',
                    'is_past': False,
                    'is_current': True,
                    'is_future': False,
                },
            ],
        }

    def test_retrieve(self, api_client, settings, season_2024, placeholder_user_expected_json):
        response = api_client.get(self.reverse_api_url(url=self.retrieve_url, pk=season_2024.pk))

        assert response.status_code == 200
        assert response.data == {
            'created_by': placeholder_user_expected_json(settings.DEFAULT_USER_TIME_ZONE),
            'updated_by': None,
            'created_at': self.format_datetime(season_2024.created_at, tz=settings.DEFAULT_USER_TIME_ZONE),
            'updated_at': self.format_datetime(season_2024.updated_at, tz=settings.DEFAULT_USER_TIME_ZONE),
            'id': season_2024.id,
            'start': '2024-03-31',
            'end': '2024-10-31',
            'is_past': True,
            'is_current': False,
            'is_future': False,
        }
