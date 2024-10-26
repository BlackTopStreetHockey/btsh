import pytest


@pytest.mark.django_db
class TestTeamModel:
    def test_to_str(self, corlears_hookers):
        assert str(corlears_hookers) == 'Corlears Hookers'
