from api.utils.testing import BaseTest


class TestGameDayViewSet(BaseTest):
    list_url = 'games:gameday-list'
    retrieve_url = 'games:gameday-detail'

    def test_list(self, api_client, settings, game_day1_2024, game_day2_2024, season_2024_expected_json,
                  butchers_expected_json, corlears_hookers_expected_json, lbs_expected_json, denim_demons_expected_json,
                  placeholder_user_expected_json):
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
                    'created_at': self.format_datetime(game_day1_2024.created_at, tz=settings.DEFAULT_USER_TIME_ZONE),
                    'updated_at': self.format_datetime(game_day1_2024.updated_at, tz=settings.DEFAULT_USER_TIME_ZONE),
                    'id': game_day1_2024.id,
                    'day': '2024-04-07',
                    'season': season_2024_expected_json(
                        is_past=True, is_current=False, is_future=False, tz=settings.DEFAULT_USER_TIME_ZONE
                    ),
                    'opening_team': butchers_expected_json(
                        tz=settings.DEFAULT_USER_TIME_ZONE, logo_prefix='http://testserver'
                    ),
                    'closing_team': corlears_hookers_expected_json(
                        tz=settings.DEFAULT_USER_TIME_ZONE, logo_prefix='http://testserver'
                    ),
                },
                {
                    'created_by': placeholder_user_expected_json(settings.DEFAULT_USER_TIME_ZONE),
                    'updated_by': None,
                    'created_at': self.format_datetime(game_day2_2024.created_at, tz=settings.DEFAULT_USER_TIME_ZONE),
                    'updated_at': self.format_datetime(game_day2_2024.updated_at, tz=settings.DEFAULT_USER_TIME_ZONE),
                    'id': game_day2_2024.id,
                    'day': '2024-04-14',
                    'season': season_2024_expected_json(
                        is_past=True, is_current=False, is_future=False, tz=settings.DEFAULT_USER_TIME_ZONE
                    ),
                    'opening_team': lbs_expected_json(
                        tz=settings.DEFAULT_USER_TIME_ZONE, logo_prefix='http://testserver'
                    ),
                    'closing_team': denim_demons_expected_json(
                        tz=settings.DEFAULT_USER_TIME_ZONE, logo_prefix='http://testserver'
                    ),
                },
            ],
        }

    def test_retrieve(self, api_client, settings, game_day1_2024, season_2024_expected_json, butchers_expected_json,
                      corlears_hookers_expected_json, placeholder_user_expected_json):
        response = api_client.get(self.reverse_api_url(url=self.retrieve_url, pk=game_day1_2024.pk))

        assert response.status_code == 200
        assert response.data == {
            'created_by': placeholder_user_expected_json(settings.DEFAULT_USER_TIME_ZONE),
            'updated_by': None,
            'created_at': self.format_datetime(game_day1_2024.created_at, tz=settings.DEFAULT_USER_TIME_ZONE),
            'updated_at': self.format_datetime(game_day1_2024.updated_at, tz=settings.DEFAULT_USER_TIME_ZONE),
            'id': game_day1_2024.id,
            'day': '2024-04-07',
            'season': season_2024_expected_json(
                is_past=True, is_current=False, is_future=False, tz=settings.DEFAULT_USER_TIME_ZONE,
            ),
            'opening_team': butchers_expected_json(
                tz=settings.DEFAULT_USER_TIME_ZONE, logo_prefix='http://testserver'
            ),
            'closing_team': corlears_hookers_expected_json(
                tz=settings.DEFAULT_USER_TIME_ZONE, logo_prefix='http://testserver'
            ),
        }
