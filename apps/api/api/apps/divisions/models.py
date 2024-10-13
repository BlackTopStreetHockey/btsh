from django.db import models

from common.models import BaseModel


class Division(BaseModel):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name
