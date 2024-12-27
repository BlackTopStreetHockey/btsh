from common.resources import BaseModelResource
from .models import Division


class DivisionResource(BaseModelResource):
    class Meta(BaseModelResource.Meta):
        model = Division
        fields = BaseModelResource.Meta.fields + ('name',)
