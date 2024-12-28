from django.db import models

from common.models import BaseModel


class Division(BaseModel):
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name
    
    @property
    def short_name(self):
        return self.name.replace("Division", '').strip()

