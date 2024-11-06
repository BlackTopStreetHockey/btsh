from django.db import models


BASE_MODEL_FIELDS = ('created_by', 'updated_by', 'created_at', 'updated_at')


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        'users.User', on_delete=models.PROTECT, null=True, blank=True, related_name='created_%(app_label)s_%(class)s'
    )
    updated_by = models.ForeignKey(
        'users.User', on_delete=models.PROTECT, null=True, blank=True, related_name='updated_%(app_label)s_%(class)s'
    )

    class Meta:
        abstract = True
