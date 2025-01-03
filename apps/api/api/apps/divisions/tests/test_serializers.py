from api.utils.testing import BaseTest

from divisions.serializers import DivisionReadOnlySerializer


class TestDivisionReadOnlySerializer(BaseTest):
    def test_serialize(self, division1, division1_expected_json):
        s = DivisionReadOnlySerializer(division1)

        self.assert_data(s.data, division1_expected_json)
