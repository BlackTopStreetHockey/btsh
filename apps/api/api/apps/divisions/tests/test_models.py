import pytest
from django.core.exceptions import ValidationError

from api.utils.testing import BaseTest


class TestDivisionModel(BaseTest):
    def test_name_uniq(self, division1, division_factory):
        with pytest.raises(ValidationError) as e:
            division_factory(name=division1.name)
        assert e.value.message_dict == {'name': ['Division with this Name already exists.']}

    def test_to_str(self, division1):
        assert str(division1) == 'Division 1'
