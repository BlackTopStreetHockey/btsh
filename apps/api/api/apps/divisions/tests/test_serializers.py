from api.utils.testing import BaseTest

from divisions.serializers import DivisionReadOnlySerializer


class TestDivisionReadOnlySerializer(BaseTest):
    def test_serialize(self, division1, placeholder_user):
        s = DivisionReadOnlySerializer(division1)

        assert s.data == {
            'created_by': self.format_created_by_updated_by(placeholder_user),
            'updated_by': None,
            'created_at': self.format_datetime(division1.created_at),
            'updated_at': self.format_datetime(division1.updated_at),
            'id': division1.id,
            'name': 'Division 1',
        }
