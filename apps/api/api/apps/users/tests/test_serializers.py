import pytest

from api.utils.testing import BaseTest
from users.serializers import UserReadOnlySerializer


@pytest.mark.django_db
class TestUserReadOnlySerializer(BaseTest):
    def test_serialize(self, wgretzky):
        s = UserReadOnlySerializer(wgretzky)

        assert s.data == {
            'id': wgretzky.id,
            'first_name': 'Wayne',
            'last_name': 'Gretzky',
            'full_name': 'Wayne Gretzky',
            'date_joined': self.format_datetime(wgretzky.date_joined),
        }
