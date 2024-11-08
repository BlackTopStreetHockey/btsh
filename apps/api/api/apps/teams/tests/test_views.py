from api.utils.testing import BaseTest


class TestTeamViewSet(BaseTest):
    list_url = 'teams:team-list'
    retrieve_url = 'teams:team-detail'

    def test_list(self, api_client, settings, corlears_hookers_expected_json, lbs_expected_json):
        response = api_client.get(self.reverse_api_url(url=self.list_url))

        assert response.status_code == 200
        assert response.data == {
            'count': 2,
            'next': None,
            'previous': None,
            'results': [
                corlears_hookers_expected_json(tz=settings.DEFAULT_USER_TIME_ZONE, logo_prefix='http://testserver'),
                lbs_expected_json(tz=settings.DEFAULT_USER_TIME_ZONE, logo_prefix='http://testserver'),
            ],
        }

    def test_retrieve(self, api_client, settings, corlears_hookers, corlears_hookers_expected_json):
        response = api_client.get(self.reverse_api_url(url=self.retrieve_url, pk=corlears_hookers.pk))

        assert response.status_code == 200
        assert response.data == corlears_hookers_expected_json(
            tz=settings.DEFAULT_USER_TIME_ZONE, logo_prefix='http://testserver'
        )
