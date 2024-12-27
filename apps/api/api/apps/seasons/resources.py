from common.resources import BaseModelResource
from .models import Season


class SeasonResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        model = Season
        fields = BaseModelResource.Meta.fields + ('start', 'end')
