from import_export import resources

from common.models import BASE_MODEL_FIELDS


class BaseModelResource(resources.ModelResource):

    def _dehydrate_user(self, user):
        """
        Django requires a unique username when creating a user and we'll almost always set username and email to the
        same values so username can effectively be used as the primary key. There is still an integer PK but we need
        something a bit more human friendly in the exported data.
        """
        return user.username if user else None

    def dehydrate_created_by(self, obj):
        return self._dehydrate_user(obj.created_by)

    def dehydrate_updated_by(self, obj):
        return self._dehydrate_user(obj.updated_by)

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
        fields = ('id', *BASE_MODEL_FIELDS)
