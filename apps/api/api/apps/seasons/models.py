from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from common.models import BaseModel


class Season(BaseModel):
    DATE_FORMAT = '%m/%d/%Y'

    start = models.DateField()
    end = models.DateField()

    @property
    def start_formatted(self):
        return self.start.strftime(self.DATE_FORMAT)

    @property
    def end_formatted(self):
        return self.end.strftime(self.DATE_FORMAT)

    @property
    def is_past(self):
        return timezone.now().date() > self.end

    @property
    def is_current(self):
        return self.start <= timezone.now().date() <= self.end

    @property
    def is_future(self):
        return timezone.now().date() < self.start

    def clean(self):
        super().clean()
        if self.start and self.end and self.end <= self.start:
            raise ValidationError({
                'start': 'Start date must be before end date.',
                'end': 'End date must be after start date.'
            })

    def __str__(self):
        return f'{self.start_formatted} - {self.end_formatted} Season'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('start', 'end'), name='start_end_uniq')
        ]
