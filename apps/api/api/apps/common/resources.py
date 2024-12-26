from import_export import resources


class BaseModelResource(resources.ModelResource):

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
