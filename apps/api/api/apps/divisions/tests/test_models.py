import pytest


@pytest.mark.django_db
class TestDivisionModel:
    def test_to_str(self, division1):
        assert str(division1) == 'Division 1'
