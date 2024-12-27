from django import forms
from django.db import models
from import_export import resources, widgets


class BaseModelResource(resources.ModelResource):

    @classmethod
    def widget_kwargs_for_field(cls, field_name, django_field):
        kwargs = super().widget_kwargs_for_field(field_name, django_field)
        # Ensure booleans are handled as True/False instead of the 0/1 default
        if isinstance(django_field, models.BooleanField):
            kwargs.update({'coerce_to_string': False})
        return kwargs

    def __init__(self, user=None, **kwargs):
        # Exporting seems to init the resource class w/o passing the resource kwargs hence user needing to be none here
        self.user = user
        super().__init__(**kwargs)

    def save_instance(self, instance, is_create, row, **kwargs):
        # Other hooks either don't have is_create handy (before_save_instance) or don't run on bulk (do_instance_save)
        if is_create:
            instance.created_by = self.user
        else:
            instance.updated_by = self.user
        return super().save_instance(instance, is_create, row, **kwargs)

    class Meta:
        clean_model_instances = True
        model = None
        # Omitting BASE_MODEL_FIELDS for now since end users don't need to know about them
        fields = ('id',)
        skip_unchanged = True


class EmailWidget(widgets.CharWidget):
    def clean(self, value, row=None, **kwargs):
        val = super().clean(value, row, **kwargs)
        if val:
            return forms.EmailField().clean(val).lower()
        return val
