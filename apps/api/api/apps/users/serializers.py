from rest_framework import serializers

from .models import User


class UserReadOnlySerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj):
        return obj.get_full_name()

    class Meta:
        model = User
        # Intentionally omit username/email so we don't include more PII than we need to
        fields = ('id', 'first_name', 'last_name', 'full_name', 'date_joined', 'gender', 'get_gender_display')
