from rest_framework import serializers

from users.serializers import UserReadOnlySerializer


class BaseReadOnlyModelSerializer(serializers.ModelSerializer):
    created_by = UserReadOnlySerializer()
    updated_by = UserReadOnlySerializer()

    class Meta:
        fields = ('created_by', 'updated_by', 'created_at', 'updated_at', 'id')
        read_only_fields = ('created_by', 'updated_by', 'created_at', 'updated_at')
