from rest_framework import serializers

from common.models import BASE_MODEL_FIELDS


class DynamicFieldsModelSerializerMixin:
    """Reference: https://www.django-rest-framework.org/api-guide/serializers/#dynamically-modifying-fields"""

    def __init__(self, *args, **kwargs):
        include = kwargs.pop('include', None)
        exclude = kwargs.pop('exclude', None)
        super().__init__(*args, **kwargs)

        if include:
            for field_name in set(self.fields) - set(include):
                self.fields.pop(field_name, None)

        if exclude:
            for field_name in exclude:
                self.fields.pop(field_name, None)


class BaseModelSerializer(DynamicFieldsModelSerializerMixin, serializers.ModelSerializer):
    class Meta:
        fields = (*BASE_MODEL_FIELDS, 'id')
        read_only_fields = (*BASE_MODEL_FIELDS,)
